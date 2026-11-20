"""Source-specific parsers and conservative SIP/RTP metrics."""
from collections import Counter, defaultdict
import csv
from dataclasses import dataclass
import json
import math
from pathlib import Path
import re
import statistics
import subprocess

from .model import MEDIA, PBX_IP, RTP_MIN, RTP_MAX, SIPP_IP, record


def read_rows(path, delimiter=";"):
    if not path or not path.is_file():
        return []
    with path.open(newline="", errors="replace") as stream:
        return list(csv.DictReader(stream, delimiter=delimiter))


def number(value, cast=float):
    try:
        result = cast(value)
    except (ValueError, TypeError, OverflowError):
        return None
    return result if math.isfinite(result) and result >= 0 else None


def percentile(values, percent):
    if not values:
        return None
    return sorted(values)[math.ceil(percent * len(values)) - 1]


def sipp_metrics(root, load):
    rows = read_rows(root / "sipp-stats.csv")
    last = rows[-1] if rows else {}
    attempts = number(last.get("OutgoingCall(C)"), int)
    successful = number(last.get("SuccessfulCall(C)"), int)
    failed = number(last.get("FailedCall(C)"), int)
    active = [value for row in rows if (value := number(row.get("CurrentCall"), int)) is not None]
    sipp = "sipp_csv"
    direction = "uac_to_uas"
    out = {
        "call_attempts": record(attempts, "count", sipp, direction),
        "successful_calls": record(successful, "count", sipp, direction),
        "failed_calls": record(failed, "count", sipp, direction),
        "scenario_success_rate": record(
            successful / attempts if attempts and successful is not None else None,
            "ratio", sipp, direction),
        "cps_configured": record(load.cps, "calls_per_sec", "run_snapshot", direction),
        "cps_achieved": record(number(last.get("CallRate(C)")), "calls_per_sec", sipp, direction),
        "concurrent_calls_peak": record(max(active, default=None), "count",
                                        "sipp_csv_sampled", "lab_call"),
        "sip_retransmits": record(number(last.get("Retransmissions(C)"), int), "count", sipp, "tx_rx"),
        "sip_timeouts": record(number(last.get("FailedTimeoutOnRecv(C)"), int), "count", sipp, "rx"),
    }
    trace = read_rows(next(iter(sorted(root.glob("*_rtt.csv"))), None))
    values = [value for row in trace if row.get("rtd_no") in ("1", "invite")
              if (value := number(row.get("response_time_ms"))) is not None]
    for label, result in (("p50", percentile(values, 0.5)), ("p95", percentile(values, 0.95)),
                          ("max", max(values, default=None))):
        out[f"call_setup_latency_{label}_ms"] = record(result, "ms", "sipp_rtt", direction)
    return out


def json_lines(path):
    if not path.is_file():
        return []
    with path.open(errors="replace") as stream:
        return [json.loads(line) for line in stream if line.endswith("\n")]


def pbx_metrics(root, trial_id):
    frames = json_lines(root / "ami.jsonl")
    ready = any(frame.get("ready") for frame in frames)
    correlation = {frame["uniqueid"]: frame["sipcallid"] for frame in frames
                   if frame.get("runid") == trial_id and frame.get("uniqueid")
                   and frame.get("sipcallid") and frame.get("userevent") == "CallPathCorrelation"}
    events = []
    related = {frame["linkedid"]: correlation[frame["uniqueid"]] for frame in frames
               if frame.get("uniqueid") in correlation and frame.get("linkedid")}
    for frame in frames:
        call_id = correlation.get(frame.get("uniqueid")) or related.get(frame.get("linkedid"))
        if call_id or frame.get("runid") == trial_id:
            events.append({**frame, "call_id": frame.get("sipcallid") or call_id})
    causes = Counter(event["cause"] for event in events if event.get("event") == "Hangup"
                     and event.get("uniqueid") in correlation and event.get("cause"))
    result = {"hangup_causes": record(dict(causes) if correlation and causes else None,
                                     "count_by_cause", "asterisk_ami_cel", "pbx_channel"),
              "pbx_call_ids_correlated": record(len(correlation) if ready else None,
                                               "count", "asterisk_ami", "pbx_channel")}
    for marker in ("DTMF", "Transfer"):
        confirmed = {event["call_id"] for event in events if event.get("call_id") and (
            event.get("userevent") == f"CallPath{marker}" or (
                marker == "DTMF" and event.get("event") == "DTMFEnd"
                and event.get("direction") == "Received" and event.get("digit") == "#"
            )
        )}
        result[f"pbx_{marker.lower()}_confirmed"] = record(
            len(confirmed) if ready else None, "count", "asterisk_ami", "pbx_channel")
    return result, events


@dataclass(frozen=True)
class Packet:
    at: float
    sequence: int
    timestamp: int
    payload: bytes


def rtp_decode(raw, at, sport, dport):
    """Decode the configured PCMU RTP payload on the PBX RTP port range."""
    if not any(RTP_MIN <= port <= RTP_MAX for port in (sport, dport)):
        return None
    if len(raw) < 12 or raw[0] >> 6 != 2 or raw[1] & 127 != MEDIA["payload_type"]:
        return None
    offset = 12 + 4 * (raw[0] & 15)
    if raw[0] & 16:
        if len(raw) < offset + 4:
            return None
        offset += 4 + 4 * int.from_bytes(raw[offset + 2:offset + 4], "big")
    end = len(raw) - (raw[-1] if raw[0] & 32 else 0)
    if end <= offset:
        return None
    return (sport, dport, int.from_bytes(raw[8:12], "big")), Packet(
        at, int.from_bytes(raw[2:4], "big"), int.from_bytes(raw[4:8], "big"), raw[offset:end])


def packets(root, name):
    path = root / f"{name}.pcap"
    log = root / f"{name}.log"
    stderr = log.read_text(errors="replace") if log.exists() else ""
    drops = re.search(r"(\d+) packets? dropped by kernel", stderr)
    captured = re.search(r"(\d+) packets? captured", stderr)
    filtered = re.search(r"(\d+) packets? received by filter", stderr)
    if (not path.is_file() or not captured or not drops or not filtered
            or int(drops[1]) or int(captured[1]) != int(filtered[1])):
        return None, None, "Capture missing, incomplete, or reported kernel drops"
    try:
        result = subprocess.run(
            ["/usr/bin/tshark", "-n", "-r", str(path), "-Y", "udp", "-T", "fields",
             "-E", "occurrence=f", "-e", "frame.time_epoch", "-e", "udp.srcport",
             "-e", "udp.dstport", "-e", "udp.payload", "-e", "sip.Status-Code"],
            text=True, capture_output=True, timeout=45, check=True)
    except (OSError, subprocess.SubprocessError) as exc:
        return None, None, f"tshark could not decode capture ({type(exc).__name__})"
    streams = defaultdict(list)
    codes = Counter()
    for line in result.stdout.splitlines():
        try:
            at, sport, dport, raw, code = line.split("\t")
            if code:
                codes[code] += 1
            if raw and (decoded := rtp_decode(bytes.fromhex(raw.replace(":", "")),
                                              float(at), int(sport), int(dport))):
                key, packet = decoded
                streams[key].append(packet)
        except ValueError:
            continue
    return streams, codes, None


def identity(packet):
    return packet.sequence, packet.timestamp


def jitter_ms(packets):
    if len(packets) < 2:
        return None
    jitter = 0
    for first, second in zip(packets, packets[1:]):
        ticks = (second.timestamp - first.timestamp + 2**31) % 2**32 - 2**31
        difference = abs((second.at - first.at) * MEDIA["clock_hz"] - ticks)
        jitter += (difference - jitter) / 16
    return jitter * 1000 / MEDIA["clock_hz"]


def stream_metrics(sender, receiver):
    expected = {identity(packet) for packet in sender}
    observed = {identity(packet) for packet in receiver}
    matched = {identity(packet): packet for packet in reversed(receiver)
               if identity(packet) in expected}
    return {
        "sent": len(expected),
        "received": len(observed & expected),
        "missing": len(expected - observed),
        "duplicates": len(receiver) - len(observed),
        "unmatched_received": len(observed - expected),
        "jitter_ms": jitter_ms(sorted(matched.values(), key=lambda packet: packet.at)),
        "payload_sizes": sorted({len(packet.payload) for packet in sender}),
    }


def echo_metrics(tx, rx):
    covered, roundtrips = 0, []
    if tx is None or rx is None:
        return None, None, 0
    rx_by_reversed_ports = defaultdict(list)
    for (source, destination, _), packets in rx.items():
        rx_by_reversed_ports[destination, source].extend(packets)
    for (source, destination, _), packets in tx.items():
        offered = defaultdict(list)
        returned = defaultdict(list)
        for packet in packets:
            offered[packet.payload].append(packet.at)
        for packet in rx_by_reversed_ports[source, destination]:
            returned[packet.payload].append(packet.at)
        covered += len(offered)
        for payload, times in offered.items():
            echoes = returned.get(payload, [])
            if len(times) == len(echoes) == 1 and 0 <= echoes[0] - times[0] <= 4:
                roundtrips.append(1000 * (echoes[0] - times[0]))
    return (len(roundtrips) / covered if covered else None,
            percentile(roundtrips, 0.5), len(roundtrips))


def pcap_metrics(root):
    captures = {name: packets(root, name) for name in ("sipp-tx", "sipp-rx", "pbx-tx", "pbx-rx")}
    metrics, details = {}, {}
    for tx, rx, direction in (("sipp-tx", "pbx-rx", "uac_to_pbx"),
                              ("pbx-tx", "sipp-rx", "pbx_to_uac")):
        sender, _, sender_error = captures[tx]
        receiver, codes, receiver_error = captures[rx]
        if codes is not None:
            metrics[f"sip_codes_{direction}"] = record(dict(codes), "count_by_code", "tshark_sip", direction)
        else:
            metrics[f"sip_codes_{direction}"] = record(None, "count_by_code", "tshark_sip", direction,
                                                       receiver_error)
        per_stream = {}
        if sender is not None and receiver is not None:
            per_stream = {"/".join(map(str, key)): stream_metrics(values, receiver.get(key, []))
                          for key, values in sender.items()}
        sent = sum(item["sent"] for item in per_stream.values())
        missing = sum(item["missing"] for item in per_stream.values())
        jitters = [item["jitter_ms"] for item in per_stream.values() if item["jitter_ms"] is not None]
        details[direction] = {"sender": tx, "receiver": rx, "streams": per_stream,
                              "capture_error": sender_error or receiver_error}
        for name, value, unit in (
            ("packet_loss", 100 * missing / sent if sent else None, "pct"),
            ("receiver_jitter", statistics.median(jitters) if jitters else None, "ms"),
        ):
            metrics[f"rtp_{name}_{direction}"] = record(value, unit, "tshark_pcap_rtp", direction,
                                                       sender_error or receiver_error)
    coverage, rtt, count = echo_metrics(captures["sipp-tx"][0], captures["sipp-rx"][0])
    metrics["echo_unique_payload_match_rate"] = record(coverage, "ratio", "tshark_echo", "round_trip")
    metrics["rtt_ms"] = record(rtt, "ms", "tshark_echo_p50_unique_payload", "round_trip",
                               "No uniquely matched PCMU echo packets")
    details["echo_matched_packets"] = count
    return metrics, details


def qdisc_metrics(data):
    values = [item for items in data.values() for item in items if item.get("kind") == "netem"]
    return {
        f"qdisc_{field}": record(sum(item[field] for item in values)
                                if values and all(isinstance(item.get(field), int) for item in values)
                                else None, "count", "tc_s_qdisc", "netem_links")
        for field in ("drops", "overlimits")
    }


def resources(samples):
    result = {}
    for side in ("sipp", "asterisk"):
        rows = [row[side] for row in samples if side in row]
        for field, unit in (("cpu_pct", "pct_one_logical_cpu"), ("rss_mib", "MiB")):
            values = [row[field] for row in rows if row.get(field) is not None]
            result[f"{side}_{field}_peak"] = record(max(values, default=None), unit, "procfs", side)
    return result
