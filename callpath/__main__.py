"""CallPath command line."""
import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import shutil
import sys

from . import runner, storage
from .model import PROFILES, SCENARIOS, Profile, TERMINAL, bounded, configure
from .report import comparison


def profiles(parser):
    for flag, kind in (
        ("delay-ms", int), ("jitter-ms", int), ("loss-pct", float), ("queue-limit", int),
        ("seed", int), ("burst-start-pct", float), ("burst-end-pct", float),
        ("reorder-pct", float), ("duplicate-pct", float),
    ):
        parser.add_argument("--" + flag, type=kind)
    for flag, choices in (("path", ("forward", "reverse", "both")),
                          ("traffic", ("all", "sip", "rtp")),
                          ("placement", ("egress", "ingress"))):
        parser.add_argument("--" + flag, choices=choices)


def profile_overrides(options):
    return {key: getattr(options, key) for key in Profile.__dataclass_fields__
              if getattr(options, key, None) is not None}


def parser():
    root = argparse.ArgumentParser(prog="callpath", description="Isolated SIP and RTP experiments")
    root.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    sub = root.add_subparsers(dest="action", required=True)
    sub.add_parser("scenarios", help="list standard experiments")
    doctor = sub.add_parser("doctor", help="verify isolated netem capability")
    profiles(doctor)
    run = sub.add_parser("run", help="execute a scenario and write evidence")
    run.add_argument("scenario", type=str.upper, choices=SCENARIOS)
    run.add_argument("--run-id", help=argparse.SUPPRESS)
    run.add_argument("--repeats", type=int)
    run.add_argument("--baseline-only", action="store_true")
    run.add_argument("--profile", choices=PROFILES)
    for arg in ("calls", "cps", "concurrency", "hold-ms", "timeout-s"):
        run.add_argument("--" + arg, type=int)
    profiles(run)
    for action in ("show", "metrics", "artifacts", "cancel"):
        command = sub.add_parser(action)
        command.add_argument("run_id")
    comp = sub.add_parser("compare", help="compare compatible run reports")
    comp.add_argument("run_id")
    comp.add_argument("baseline_run_id")
    sub.add_parser("janitor", help="verify teardown and recover interrupted run records")
    prune = sub.add_parser("prune", help="list expired terminal artifacts or explicitly remove them")
    prune.add_argument("--older-than-days", type=int, default=14)
    prune.add_argument("--apply", action="store_true")
    return root


def emit(item):
    print(json.dumps(item, indent=2, sort_keys=True, allow_nan=False))


def main():
    opts = parser().parse_args()
    root = opts.artifacts.resolve()
    action = opts.action
    if action == "scenarios":
        emit(SCENARIOS)
        return 0
    if action == "doctor":
        with storage.lock(root):
            proof = runner.doctor(Profile(**({"delay_ms": 15, "traffic": "rtp"} | profile_overrides(opts))))
        emit(proof)
        return 0 if proof["ok"] else 1
    if action == "janitor":
        runner.capabilities()
        with storage.lock(root):
            proof = runner.recover(root)
        emit(proof)
        return 0 if proof["verified"] else 1
    if action == "run":
        if opts.run_id and not storage.ID.fullmatch(opts.run_id):
            raise ValueError("invalid preallocated run id")
        overrides = {name: getattr(opts, name) for name in
                     ("calls", "cps", "concurrency", "hold_ms", "timeout_s")
                     if getattr(opts, name) is not None}
        stages, shaping, repeats = configure(opts.scenario, overrides, profile_overrides(opts),
                                              opts.repeats, opts.profile, opts.baseline_only)
        return 0 if runner.experiment(root, opts.scenario, stages, shaping, repeats,
                                      opts.run_id) == "SUCCEEDED" else 1
    if action == "prune":
        bounded("older-than-days", opts.older_than_days, 1, 3650, int)
        cutoff = datetime.now(timezone.utc) - timedelta(days=opts.older_than_days)
        expired = []
        with storage.lock(root):
            for candidate in sorted(root.iterdir()):
                if (not storage.ID.fullmatch(candidate.name) or candidate.is_symlink()
                        or not (candidate / "status.json").is_file()):
                    continue
                state = storage.json_read(candidate / "status.json")
                if state["status"] in TERMINAL and datetime.fromisoformat(state["updated_at"]) < cutoff:
                    expired.append(candidate.name)
                    if opts.apply:
                        shutil.rmtree(candidate)
        emit({"applied": opts.apply, "run_ids": expired})
        return 0
    path = storage.run_path(root, opts.run_id)
    if action == "compare":
        baseline = storage.run_path(root, opts.baseline_run_id)
        result = comparison(path, baseline)
        emit(result)
        return 0 if result["compatible"] else 1
    if action == "metrics":
        emit(storage.json_read(path / "report.json")["aggregates"])
    elif action == "artifacts":
        emit(storage.json_read(path / "artifacts.json"))
    else:
        state = storage.json_read(path / "status.json")
        if action == "cancel":
            if state["status"] in TERMINAL:
                raise ValueError(f"run is already {state['status']}")
            (path / ".cancel").touch(mode=0o600)
        if (path / ".cancel").exists() and state["status"] not in TERMINAL:
            state["status"] = "CANCELLING"
        emit(state)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        print(f"callpath: {exc}", file=sys.stderr)
        sys.exit(2)
