"""Local device worker. Docker stays on the worker side of the queue."""
import argparse
import fcntl
import os
from pathlib import Path
import signal
import subprocess
import time
import uuid

import psycopg

from callpath.model import TERMINAL
from callpath.storage import ID, json_read
from service import db
from service.contracts import RunRequest

PROJECT = Path(__file__).resolve().parent.parent
LAB = PROJECT / "lab"
CLOSING = False


def handle_signal(_signum, _frame):
    global CLOSING
    CLOSING = True


def local_json(root, relative, default=None):
    path = root / relative
    return json_read(path) if path.is_file() else default


def load_evidence(root, run_id):
    path = root / run_id
    report = local_json(path, "report.json")
    snapshot = local_json(path, "snapshot.json")
    manifest = local_json(path, "artifacts.json", [])
    events = [(trial["id"], event) for trial in (report or {}).get("trials", [])
              for event in local_json(path / trial["directory"], "events.json", [])]
    return snapshot, report, manifest, events


def finish(root, run_id, token, fallback, error=None):
    state = local_json(root / run_id, "status.json", {})
    status = state.get("status", fallback)
    if status not in TERMINAL:
        status = "CLEANUP_FAILED"
    snapshot, report, artifacts, events = load_evidence(root, run_id)
    with db.connect() as conn:
        return db.finalize(conn, run_id, token, status, snapshot, report, artifacts, events,
                           error or state.get("error"))


def janitor():
    return subprocess.run([LAB, "janitor"], text=True, capture_output=True, timeout=35).returncode == 0


def reap(root):
    with db.connect() as conn:
        candidates = db.expired(conn)
    if not candidates:
        return
    inspected = subprocess.run(
        ["docker", "ps", "-a", "--filter", "label=io.callpath.run", "--format", "{{.Names}}"],
        capture_output=True, text=True, timeout=10, check=True)
    active = set(inspected.stdout.splitlines())
    for entry in candidates:
        run_id, token = entry["run_id"], entry["lease_token"]
        if not ID.fullmatch(run_id) or f"callpath-{run_id}" in active:
            continue
        existing = (root / run_id / "status.json").is_file()
        recovered = not existing or janitor()
        fallback = "FAILED" if recovered else "CLEANUP_FAILED"
        finish(root, run_id, token, fallback, "Worker lease expired")


def execute(root, job, token):
    run_id = job["run_id"]
    if job["status"] == "CANCELLING":
        finish(root, run_id, token, "CANCELLED")
        return
    request = RunRequest.model_validate(job["request"])
    retained = root / ".worker-logs"
    retained.mkdir(mode=0o700, exist_ok=True)
    with (retained / f"{run_id}.log").open("x") as stream:
        proc = subprocess.Popen([LAB, *request.lab_arguments(run_id)], stdout=stream, stderr=stream)
        next_lease = 0.0
        cancel_requested = False
        try:
            while proc.poll() is None:
                if time.monotonic() >= next_lease:
                    with db.connect() as conn:
                        state = db.heartbeat(conn, run_id, token)
                    if state is None:
                        raise RuntimeError("run lease lost")
                    cancel_requested |= CLOSING or state == "CANCELLING"
                    next_lease = time.monotonic() + 2
                status = root / run_id / "status.json"
                if cancel_requested and status.is_file():
                    (status.parent / ".cancel").touch(mode=0o600)
                time.sleep(0.2)
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=45)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
    fallback = "CANCELLED" if cancel_requested else "FAILED"
    finish(root, run_id, token, fallback,
           "Lab process did not publish a result" if not (root / run_id / "status.json").exists() else None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    root = Path(os.getenv("CALLPATH_ARTIFACTS", str(PROJECT / "artifacts"))).resolve()
    os.environ["CALLPATH_ARTIFACTS"] = str(root)
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, handle_signal)
    with (root / ".worker.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            parser.error("a worker already owns this artifact directory")
        while not CLOSING:
            token = uuid.uuid4().hex
            try:
                reap(root)
                with db.connect() as conn:
                    job = db.claim(conn, token)
                if job:
                    execute(root, job, token)
            except (OSError, ValueError, RuntimeError, psycopg.Error, subprocess.SubprocessError) as exc:
                print(f"Worker: {exc}", flush=True)
                if args.once:
                    return 1
            if args.once:
                return 0
            time.sleep(1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
