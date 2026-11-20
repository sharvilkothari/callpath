"""HTTP contract checks against a running local workbench and worker."""
from datetime import datetime, timezone
import json
import os
import time
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ORIGIN = os.environ.get("CALLPATH_API_ORIGIN", "http://127.0.0.1:8042")
TOKEN = os.environ["CALLPATH_API_TOKEN"]
TERMINAL = {"SUCCEEDED", "FAILED", "CANCELLED", "CLEANUP_FAILED", "TIMED_OUT"}


def call(path, code=200, payload=None, method="GET", authorized=True):
    headers = {"Content-Type": "application/json"}
    if authorized:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = Request(ORIGIN + path, data=None if payload is None else json.dumps(payload).encode(),
                  method=method, headers=headers)
    try:
        response = urlopen(req, timeout=10)
    except HTTPError as problem:
        response = problem
    with response:
        body = json.load(response)
        assert response.status == code, (path, code, response.status, body)
        return body


def queue(scenario, **values):
    return call("/runs", 201, {"scenario_id": scenario, "target_id": "ast_local", **values},
                method="POST")["run_id"]


def wait(run_id, states, seconds=90):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        row = call(f"/runs/{run_id}")
        if row["status"] in states:
            return row
        time.sleep(0.35)
    raise AssertionError(f"{run_id} did not reach {states}: {row['status']}")


def main():
    call("/runs", 401, authorized=False)
    assert call("/profiles")["target_id"] == "ast_local"
    call("/runs", 404, {"scenario_id": "S0", "target_id": "off-lab"}, method="POST")
    call("/runs", 422, {"scenario_id": "S0", "target_id": "ast_local",
                       "overrides": {"cps": 999}}, method="POST")
    call("/runs/invalid", 400)
    call("/runs/" + "e" * 32, 404)
    first = queue("S0", repeats=1)
    second = queue("S0", repeats=1)
    queued = queue("S3", overrides={"calls": 60})
    call(f"/runs/{queued}/cancel", 202, method="POST")
    for run_id in (first, second):
        row = wait(run_id, TERMINAL)
        assert row["status"] == "SUCCEEDED", row
        assert row["snapshot"]["target"]["host"] == "10.200.1.3"
        assert row["summary"]["cleanup"]["verified"]
        assert all(check["status"] == "PASS" for check in row["summary"]["checks"])
        params = urlencode({"metric_name": "call_attempts", "end": datetime.now(timezone.utc).isoformat()})
        sample, = call(f"/runs/{run_id}/metrics?{params}")["items"]
        assert sample["value"] == 1 and sample["source"] == "sipp_csv", sample
        artifacts = call(f"/runs/{run_id}/artifacts")["artifacts"]
        assert any(item["path"] == "report.md" and len(item["sha256"]) == 64 for item in artifacts)
        call(f"/runs/{run_id}/cancel", 409, method="POST")
    cancelled = wait(queued, TERMINAL)
    assert cancelled["status"] == "CANCELLED", cancelled
    compare = call(f"/runs/compare?run_id={second}&baseline_run_id={first}")
    assert compare["compatible"] and compare["deltas"]
    call(f"/runs/compare?run_id={first}&baseline_run_id={queued}", 409)
    running = queue("S3", overrides={"calls": 60})
    wait(running, {"RUNNING"})
    call(f"/runs/{running}/cancel", 202, method="POST")
    row = wait(running, TERMINAL)
    assert row["status"] == "CANCELLED" and row["summary"]["cleanup"]["verified"], row
    print("API auth, validation, execution, queue and active cancellation, metrics, artifacts, and compare passed")


if __name__ == "__main__":
    main()
