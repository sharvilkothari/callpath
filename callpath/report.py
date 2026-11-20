"""Condition aggregates, compatibility checks, and interpretation."""
from collections import defaultdict
import json
import statistics

from . import storage

LATENCY = "call_setup_latency_p95_ms"
SUCCESS = "scenario_success_rate"


def spread(values, n):
    return {"n": len(values), "expected_n": n,
            "mean": statistics.fmean(values) if values else None,
            "median": statistics.median(values) if values else None,
            "min": min(values, default=None), "max": max(values, default=None),
            "sample_stdev": statistics.stdev(values) if len(values) > 1 else None}


def aggregate(trials, repeats):
    groups = defaultdict(list)
    for trial in trials:
        groups[(trial["condition"], trial["stage"])].append(trial)
    out = {}
    for (condition, stage), group in groups.items():
        records = [trial.get("metrics", {}) for trial in group if trial["status"] == "SUCCEEDED"]
        keys = sorted({key for record in records for key in record})
        results = {}
        for key in keys:
            occurrences = [record[key] for record in records if key in record]
            items = [record["value"] for record in occurrences
                     if isinstance(record["value"], (int, float))]
            if occurrences and all(isinstance(occurrence["value"], dict) or occurrence["unit"].startswith("count_by")
                                   for occurrence in occurrences):
                labels = sorted({label for occurrence in occurrences
                                 for label in (occurrence["value"] or {})})
                measured = [occurrence["value"] for occurrence in occurrences
                            if occurrence["value"] is not None]
                results[key] = {**spread([], repeats), "n": len(measured),
                                "count_spreads": {label: spread(
                                    [values.get(label, 0) for values in measured], repeats)
                                    for label in labels}}
            else:
                results[key] = spread(items, repeats)
            results[key].update({field: occurrences[0][field] for field in ("unit", "source", "direction")})
        out.setdefault(condition, {})[stage] = results
    return out


def check(label, observed, operator, value, complete=True):
    if observed is None or not complete:
        state = "INSUFFICIENT_EVIDENCE"
    else:
        passed = observed >= value if operator == ">=" else observed <= value
        state = "PASS" if passed else "FAIL"
    return {"check": label, "observed": observed, "operator": operator,
            "threshold": value, "status": state}


def acceptance(snapshot, aggregates):
    checks = []
    scenario = snapshot["scenario"]["id"]
    expected = snapshot["repeats"]
    for condition, stages in aggregates.items():
        for stage, values in stages.items():
            tag = f"{condition}/{stage}"
            s = values.get(SUCCESS, {})
            observed = s.get("min")
            floor = 0.99 if condition == "baseline" else (0.8 if scenario == "S5" else 0.95)
            checks.append(check(f"{tag} minimum scenario success", observed, ">=", floor,
                                s.get("n") == expected))
            if scenario == "S0":
                correlated = values.get("pbx_call_ids_correlated", {})
                checks.append(check(f"{tag} correlated PBX calls", correlated.get("min"),
                                    ">=", 1, correlated.get("n") == expected))
            if scenario == "S3":
                channels = values.get("asterisk_channels_remaining", {})
                checks.append(check(f"{tag} remaining PBX channels", channels.get("max"),
                                    "<=", 0, channels.get("n") == expected))
            if scenario == "S1":
                latency = values.get(LATENCY, {})
                available = latency.get("n", 0) >= 2 and latency.get("n") == expected
                observed = latency["max"] - latency["min"] if available else None
                checks.append(check(f"{tag} setup p95 spread (ms)", observed, "<=", 40))
            if stage in ("dtmf", "transfer"):
                confirmations = values.get(f"pbx_{stage}_confirmed", {})
                calls = next(entry["load"]["calls"] for entry in snapshot["scenario"]["stages"]
                             if entry["label"] == stage)
                checks.append(check(f"{tag} PBX confirmations", confirmations.get("min"), ">=",
                                    calls, confirmations.get("n") == expected))
            if scenario == "S7":
                echo = values.get("echo_unique_payload_match_rate", {})
                floor = 0.8 if condition == "baseline" else 0.60
                checks.append(check(f"{tag} minimum unique payload echo coverage", echo.get("min"),
                                    ">=", floor, echo.get("n") == expected))
    delay = snapshot["profile"]["delay_ms"]
    if scenario in ("S4", "S5", "S7") and "impaired" in aggregates:
        profile = snapshot["profile"]
        for stage, values in aggregates["impaired"].items():
            baseline = aggregates.get("baseline", {}).get(stage, {})
            if profile["traffic"] != "sip":
                directions = (("uac_to_pbx", "forward"), ("pbx_to_uac", "reverse"))
                for direction, path in directions:
                    if profile["path"] not in (path, "both"):
                        continue
                    key = f"rtp_packet_loss_{direction}"
                    first, second = baseline.get(key, {}), values.get(key, {})
                    adequate = all(item.get("n") == expected for item in (first, second))
                    difference = second["median"] - first["median"] if adequate else None
                    if profile["loss_pct"]:
                        checks.append(check(f"impaired/{stage} {direction} median loss delta (pp)",
                                            difference, "<=", profile["loss_pct"] + 5))
            if delay and profile["traffic"] != "rtp":
                first, second = baseline.get(LATENCY, {}), values.get(LATENCY, {})
                adequate = all(item.get("n") == expected for item in (first, second))
                difference = second["median"] - first["median"] if adequate else None
                factor = 2 if profile["path"] == "both" else 1
                checks.append(check(f"impaired/{stage} median setup p95 delta (ms)", difference,
                                    "<=", (delay + 3 * profile["jitter_ms"]) * factor + 100))
    return checks


def compare_values(baseline, subject):
    deltas = {}
    for stage in sorted(baseline.keys() & subject.keys()):
        a, b = baseline[stage], subject[stage]
        for name in sorted(a.keys() & b.keys()):
            left, right = a[name], b[name]
            if any(left[key] != right[key] for key in ("unit", "source", "direction")):
                continue
            first, second = left["median"], right["median"]
            deltas[f"{stage}/{name}"] = {
                "median_delta": second - first if first is not None and second is not None else None,
                "baseline": left, "subject": right,
            }
    return deltas


def compatibility_warnings(snapshot, reference):
    keys = ("scenario", "target", "media", "tools", "runtime", "file_hashes")
    warnings = [f"{key} differs" for key in keys if snapshot[key] != reference[key]]
    shaping = ("queue_limit", "placement", "path", "traffic")
    warnings.extend(f"profile.{key} differs" for key in shaping
                    if snapshot["profile"][key] != reference["profile"][key])
    return warnings


def comparison(path, baseline_path):
    if path == baseline_path:
        raise ValueError("choose two runs")
    for run_path in (path, baseline_path):
        if storage.json_read(run_path / "status.json")["status"] != "SUCCEEDED":
            raise ValueError("both runs must be complete")
    snapshot = storage.json_read(path / "snapshot.json")
    reference = storage.json_read(baseline_path / "snapshot.json")
    warnings = compatibility_warnings(snapshot, reference)
    if warnings:
        return {"compatible": False, "warnings": warnings, "deltas": {}}
    left = storage.json_read(baseline_path / "report.json")["aggregates"].get("baseline", {})
    right_conditions = storage.json_read(path / "report.json")["aggregates"]
    right = right_conditions.get("impaired", right_conditions.get("baseline", {}))
    if not left or not right:
        return {"compatible": False, "warnings": ["No completed comparison groups"], "deltas": {}}
    deltas = compare_values(left, right)
    return {"compatible": True, "warnings": [], "deltas": deltas}


def summarize(path, trials, proof, state):
    snapshot = storage.json_read(path / "snapshot.json")
    aggregates = aggregate(trials, snapshot["repeats"])
    checks = acceptance(snapshot, aggregates)
    notes = [
        "Experiments describe the isolated local Asterisk lab. Carrier, production and conversational quality conclusions require separate evidence.",
        "The seeded netem sequence depends on packet order and the host schedule.",
        "Qdisc drops may include both configured impairment and queue saturation.",
        "Setup timings are SIP INVITE to first successful response. Echo RTT requires uniquely matched round-trip payloads.",
        "RTP loss uses sender-to-receiver identity matching. Jitter is the median of final RFC 3550 estimates across streams.",
        "CPU utilization is process-based, in units of one logical CPU.",
    ]
    if snapshot["repeats"] < 5:
        notes.append("Fewer than five planned repeats per condition; treat observed spread as preliminary.")
    result = {
        "run_id": path.name, "status": state, "snapshot_sha256": storage.sha256(path / "snapshot.json"),
        "trials": trials, "aggregates": aggregates, "checks": checks,
        "comparison": compare_values(aggregates.get("baseline", {}), aggregates.get("impaired", {})),
        "cleanup": proof, "notes": notes,
    }
    storage.json_write(path / "report.json", result)

    def format_value(value):
        return "—" if value is None else f"{value:.4g}"

    lines = [f"# CallPath {snapshot['scenario']['id']} run", "",
             f"Run `{path.name}` · **{state}** · cleanup {'verified' if proof['verified'] else 'unverified'}",
             "", f"Target {snapshot['target']['host']} over UDP · PCMU, 20 ms · {snapshot['repeats']} planned repeats",
             "", f"Shaping profile `{json.dumps(snapshot['profile'], sort_keys=True)}`",
             "", "## Results by condition", ""]
    for condition, stages in aggregates.items():
        for stage, data in stages.items():
            lines += [f"### {condition} / {stage}", "",
                      "| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |",
                      "| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |"]
            for name, row in data.items():
                if "count_spreads" in row:
                    for label, counts in row["count_spreads"].items():
                        lines.append(f"| {name} ({label}) | {format_value(counts['median'])} | "
                                     f"{format_value(counts['mean'])} | {format_value(counts['min'])}–"
                                     f"{format_value(counts['max'])} | {format_value(counts['sample_stdev'])} | "
                                     f"{counts['n']}/{counts['expected_n']} | count | {row['source']} |")
                    continue
                lines.append(f"| {name} | {format_value(row['median'])} | "
                             f"{format_value(row['mean'])} | {format_value(row['min'])}–"
                             f"{format_value(row['max'])} | {format_value(row['sample_stdev'])} | "
                             f"{row['n']}/{row['expected_n']} | {row['unit']} | {row['source']} |")
            lines.append("")
    lines += ["## Baseline comparison", "",
              "| Stage / metric | Impaired − baseline median | Unit |",
              "| --- | ---: | --- |"]
    for name, delta in result["comparison"].items():
        if delta["median_delta"] is not None:
            lines.append(f"| {name} | {format_value(delta['median_delta'])} | {delta['subject']['unit']} |")
    lines += ["", "## Acceptance", "",
              "| Check | Observed | Threshold | Result |", "| --- | ---: | ---: | --- |"]
    for item in checks:
        lines.append(f"| {item['check']} | {format_value(item['observed'])} | "
                     f"`{item['operator']} {item['threshold']}` | {item['status']} |")
    lines += ["", "## Evidence", "", "- [Run snapshot](snapshot.json)",
              "- [Machine-readable report](report.json)", "- [Artifact manifest](artifacts.json)"]
    for trial in trials:
        lines.append(f"- [{trial['directory']}]({trial['directory']}/trial.json) · {trial['status']}")
    lines += ["", "## Interpretation", ""] + [f"- {note}" for note in notes]
    storage.atomic(path / "report.md", "\n".join(lines) + "\n")
