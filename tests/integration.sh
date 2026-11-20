#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
: "${CALLPATH_ARTIFACTS:?set CALLPATH_ARTIFACTS to a dedicated Docker-shareable directory}"
mode=${1:-full}
case "$mode" in full|ingress|lifecycle) ;; *) exit 2 ;; esac

new_id() { od -An -N16 -tx1 /dev/urandom | tr -d ' \n'; }
verify() {
  "${CALLPATH_PYTHON:-python3}" - "$CALLPATH_ARTIFACTS/$1" "$2" <<'PY'
from pathlib import Path
import json
import sys

from callpath.storage import sha256

run = Path(sys.argv[1])
expected = sys.argv[2]
status = json.loads((run / "status.json").read_text())
assert status["status"] == expected, status
report = json.loads((run / "report.json").read_text())
assert report["status"] == expected, report["status"]
assert report["cleanup"]["verified"] is True, report["cleanup"]
assert report["snapshot_sha256"] == sha256(run / "snapshot.json")
items = json.loads((run / "artifacts.json").read_text())
assert items and all(item["sha256"] == sha256(run / item["path"]) for item in items)
if expected == "SUCCEEDED":
    assert report["checks"], report
    assert all(item["status"] == "PASS" for item in report["checks"]), report["checks"]
print(f"{expected} and manifest verified for {run.name}")
PY
}
run() {
  id=$(new_id)
  ./lab run "$@" --run-id "$id"
  verify "$id" SUCCEEDED
}
await_start() {
  id=$1
  tries=100
  while [ "$tries" -gt 0 ]; do
    if [ -f "$CALLPATH_ARTIFACTS/$id/status.json" ] &&
       grep -q '"status": "RUNNING"' "$CALLPATH_ARTIFACTS/$id/status.json"; then
      return
    fi
    tries=$((tries - 1))
    sleep 0.1
  done
  printf '%s\n' "Run did not start: $id" >&2
  return 1
}
if [ "$mode" = ingress ]; then
  ./lab doctor --placement ingress --path both --traffic rtp
  run S5 --placement ingress --path both --traffic rtp --calls 6 --repeats 5 --loss-pct 8
elif [ "$mode" = lifecycle ]; then
  id=$(new_id)
  if ./lab run S3 --calls 5 --hold-ms 8000 --timeout-s 2 --run-id "$id"; then exit 1; fi
  verify "$id" TIMED_OUT

  id=$(new_id)
  ./lab run S3 --calls 50 --run-id "$id" &
  job=$!
  await_start "$id"
  ./lab cancel "$id"
  if wait "$job"; then exit 1; fi
  verify "$id" CANCELLED

  id=$(new_id)
  ./lab run S3 --calls 50 --run-id "$id" &
  job=$!
  await_start "$id"
  trials=100
  while [ "$trials" -gt 0 ] && [ ! -s "$CALLPATH_ARTIFACTS/$id/baseline-soak-01/sipp-tx.pcap" ]; do
    trials=$((trials - 1))
    sleep 0.1
  done
  [ "$trials" -gt 0 ]
  docker kill --signal KILL "callpath-$id"
  if wait "$job"; then exit 1; fi
  trials=100
  while [ "$trials" -gt 0 ] && docker container inspect "callpath-$id" >/dev/null 2>&1; do
    trials=$((trials - 1))
    sleep 0.1
  done
  [ "$trials" -gt 0 ]
  ./lab janitor
  verify "$id" CANCELLED
else
  ./lab doctor
  run S0
  run S1
  run S2
  run S3
  run S4 --calls 5 --traffic sip
  baseline=$(new_id)
  ./lab run S4 --calls 5 --traffic sip --baseline-only --run-id "$baseline"
  verify "$baseline" SUCCEEDED
  ./lab compare "$id" "$baseline" > "$CALLPATH_ARTIFACTS/comparison.json"
  run S5 --calls 8 --traffic rtp --loss-pct 8
  run S6
  run S7 --calls 5
fi
