"""Atomic local records and artifact manifests."""
import contextlib
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

ID = re.compile(r"[a-f0-9]{32}\Z")


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def json_read(path):
    with path.open() as stream:
        return json.load(stream)


def atomic(path, contents):
    fd, tmp = tempfile.mkstemp(prefix=".write-", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            stream.write(contents)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        Path(tmp).unlink(missing_ok=True)


def json_write(path, value):
    atomic(path, json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def immutable(path, value):
    with path.open("x") as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    path.chmod(0o444)


def run_path(root, run_id):
    if not ID.fullmatch(run_id):
        raise ValueError("expected a 32-character hexadecimal run id")
    candidate = root / run_id
    if not candidate.is_dir() or candidate.is_symlink():
        raise FileNotFoundError(f"run {run_id} does not exist")
    return candidate


@contextlib.contextmanager
def lock(root):
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    with (root / ".lab.lock").open("a") as lease:
        try:
            fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError("an experiment already holds the artifact directory lock")
        yield


def manifest(path):
    kinds = {
        ".pcap": "capture", ".log": "log", ".jsonl": "events",
        ".csv": "statistics", ".json": "record", ".md": "report",
    }
    excluded = {"status.json", "artifacts.json"}
    return [{"type": kinds.get(item.suffix, "file"), "path": item.relative_to(path).as_posix(),
             "sha256": sha256(item), "size_bytes": item.stat().st_size}
            for item in sorted(path.rglob("*")) if item.is_file() and not item.is_symlink()
            and not item.name.startswith(".") and item.name not in excluded]
