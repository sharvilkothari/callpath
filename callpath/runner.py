"""Local execution, process supervision, and verifiable teardown."""
from contextlib import ExitStack, contextmanager
from dataclasses import asdict
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import sys
import time
import uuid

from . import metrics, storage
from .model import MEDIA, PBX_IP, SIP_PORT, TERMINAL, record
from .report import summarize

ROOT = Path("/opt/callpath")
WORK = Path("/run/callpath-work")
HELPER = ("/usr/bin/sudo", "-n", "/usr/bin/python3", "-I", "/opt/callpath/network/helper.py")


class Cancelled(Exception):
    pass


class Deadline(Exception):
    pass


def invoke(*arguments, payload=None, timeout=20, check=True):
    result = subprocess.run(
        (*HELPER, *arguments), cwd="/", input=json.dumps(payload) if payload is not None else "",
        text=True, capture_output=True, timeout=timeout)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"{arguments[0]} failed")
    return result


def cleanup():
    try:
        result = invoke("cleanup", timeout=24, check=False)
        if result.stdout.strip():
            return json.loads(result.stdout)
        error = result.stderr.strip() or "No teardown verification returned"
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        error = str(exc)
    return {"verified": False, "remaining": None, "errors": [error]}


def capabilities():
    if sys.platform != "linux" or not WORK.is_dir() or not Path(HELPER[0]).is_file():
        raise RuntimeError("run the Linux lab with ./lab or its documented container entry point")


def version(argv, marker):
    result = subprocess.run(argv, text=True, capture_output=True, timeout=8)
    return next((line.strip() for line in (result.stdout + result.stderr).splitlines()
                 if marker.casefold() in line.casefold()), None)


def toolchain():
    tools = {
        "sipp": version(["/usr/bin/sipp", "-v"], "SIPp"),
        "asterisk": version(["/usr/sbin/asterisk", "-V"], "Asterisk"),
        "tc": version(["/usr/sbin/tc", "-V"], "iproute2"),
        "ip": version(["/usr/sbin/ip", "-V"], "iproute2"),
        "tshark": version(["/usr/bin/tshark", "-v"], "TShark"),
        "tcpdump": version(["/usr/bin/tcpdump", "--version"], "tcpdump version"),
        "kernel": platform.release(),
        "python": platform.python_version(),
    }
    missing = [name for name, value in tools.items() if value is None]
    if missing:
        raise RuntimeError("could not identify tool versions for " + ", ".join(missing))
    return tools


def snapshot(run_id, scenario, stages, profile, repeats, tools):
    config = {str(path.relative_to(ROOT)): storage.sha256(path)
              for folder in ("asterisk", "scenarios", "callpath", "network")
              for path in sorted((ROOT / folder).glob("*"))
              if path.is_file() and not path.name.startswith(".")}
    return {
        "run_id": run_id, "schema_version": 1,
        "scenario": {"id": scenario, "version": "1.0", "stages": [asdict(stage) for stage in stages]},
        "target": {"id": "ast_local", "allowlisted": True, "host": PBX_IP,
                   "transport": "UDP", "port": SIP_PORT},
        "media": MEDIA, "profile": asdict(profile), "repeats": repeats, "tools": tools,
        "runtime": {"mode": "isolated_linux_container", "machine": platform.machine(),
                    "boot_id": Path("/proc/sys/kernel/random/boot_id").read_text().strip()},
        "file_hashes": config,
    }


def ready_log(path):
    return path.exists() and "listening on " in path.read_text(errors="replace")


def pause_until(check, cancel, deadline, message, proc=None):
    while not check():
        if cancel():
            raise Cancelled
        if proc is not None and proc.poll() is not None:
            raise RuntimeError(f"{message} (exit {proc.returncode})")
        if time.monotonic() >= deadline:
            raise RuntimeError(message)
        time.sleep(0.05)


def launch(stack, *arguments, output, log, payload=None):
    proc = subprocess.Popen(
        (*HELPER, *arguments), cwd="/", start_new_session=True,
        stdin=subprocess.PIPE if payload is not None else subprocess.DEVNULL,
        stdout=stack.enter_context(output.open("wb")),
        stderr=stack.enter_context(log.open("wb")),
    )
    if payload is not None:
        proc.stdin.write(json.dumps(payload).encode())
        proc.stdin.close()
    return proc


def stop(proc, sig=signal.SIGTERM, wait=3):
    if proc is None or proc.poll() is not None:
        return
    try:
        os.killpg(proc.pid, sig)
        proc.wait(timeout=wait)
    except (ProcessLookupError, PermissionError, subprocess.TimeoutExpired):
        pass


def sample_processes(previous):
    result = {"monotonic_s": time.monotonic()}
    for path in Path("/proc").glob("[0-9]*/stat"):
        try:
            raw = path.read_text()
            _, _, command = raw[:raw.rindex(")")].partition("(")
            if command not in ("sipp", "asterisk") or path.stat().st_uid != os.getuid():
                continue
            fields = raw[raw.rindex(")") + 2:].split()
            # Ignore briefly spawned Asterisk CLI processes when the PBX is already present.
            if command in result:
                continue
            ticks = int(fields[11]) + int(fields[12])
            rss = int(fields[21]) * os.sysconf("SC_PAGE_SIZE") / (1024 * 1024)
            key = (path.parent.name, fields[19])
            prior = previous.get(key)
            cpu = None if not prior else (100 * (ticks - prior[0]) /
                                           os.sysconf("SC_CLK_TCK") /
                                           (result["monotonic_s"] - prior[1]))
            result[command] = {"pid": int(path.parent.name), "rss_mib": rss, "cpu_pct": cpu}
            previous[key] = (ticks, result["monotonic_s"])
        except (OSError, IndexError, ValueError, ZeroDivisionError):
            continue
    return result


def transfer_logs(destination):
    for entry in WORK.iterdir():
        if entry.is_file() and not entry.is_symlink() and (
            entry.suffix in (".csv", ".log") or entry.name in ("call.xml", "dtmf.xml", "transfer.xml")
        ):
            shutil.copy2(entry, destination / entry.name)


def clear_work():
    for path in WORK.iterdir():
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        else:
            path.unlink()


def trial(destination, stage, profile, cancel, result):
    destination.mkdir()
    trial_id = uuid.uuid4().hex
    result["id"] = trial_id
    storage.immutable(destination / "trial.json", {
        "id": trial_id, "stage": stage.label, "load": asdict(stage.load), "profile": asdict(profile),
    })
    initial = cleanup()
    if not initial["verified"]:
        result.update(status="CLEANUP_FAILED", cleanup=initial)
        return
    clear_work()
    result["status"] = "RUNNING"
    captures = []
    pbx = observer = sipp = None
    samples, previous, qdisc = [], {}, {}
    channel_count = None
    flow = stage.label if stage.label in ("dtmf", "transfer") else "call"
    with ExitStack() as stack:
        try:
            if cancel():
                raise Cancelled
            invoke("setup", payload=asdict(profile), timeout=60)
            pbx = launch(stack, "pbx", output=destination / "asterisk.log",
                         log=destination / "asterisk-stderr.log")
            readiness = time.monotonic() + 18

            def booted():
                result = invoke("ready", timeout=4, check=False)
                return result.returncode == 0 and "fully booted" in result.stdout.lower()

            pause_until(booted, cancel, readiness, "Asterisk did not finish booting", pbx)
            observer = launch(stack, "ami", output=destination / "ami.jsonl",
                              log=destination / "ami.log")
            pause_until(lambda: (destination / "ami.jsonl").stat().st_size > 0, cancel,
                        time.monotonic() + 5, "AMI collector could not log in", observer)
            for side in ("sipp", "pbx"):
                for direction in ("tx", "rx"):
                    name = f"{side}-{direction}"
                    log = destination / f"{name}.log"
                    proc = launch(stack, "capture", side, direction,
                                  output=destination / f"{name}.pcap", log=log)
                    captures.append(proc)
                    pause_until(lambda: ready_log(log), cancel, time.monotonic() + 5,
                                f"{name} capture did not start", proc)
            sipp = launch(stack, "sipp", output=destination / "sipp.log",
                          log=destination / "sipp-stderr.log",
                          payload={**asdict(stage.load), "flow": flow, "run_id": trial_id})
            start = time.monotonic()
            next_sample = start
            while sipp.poll() is None:
                if cancel():
                    raise Cancelled
                current = time.monotonic()
                if current - start >= stage.load.timeout_s:
                    raise Deadline
                if pbx.poll() is not None:
                    raise RuntimeError("Asterisk exited during the trial")
                if current >= next_sample:
                    samples.append(sample_processes(previous))
                    next_sample = current + 0.2
                time.sleep(0.04)
            result["sipp_exit_code"] = sipp.returncode
            if sipp.returncode not in (0, 1):
                raise RuntimeError(f"SIPp exited with code {sipp.returncode}")
            drain = time.monotonic() + max(0.25, (profile.delay_ms + 5 * profile.jitter_ms) / 1000)
            while time.monotonic() < drain:
                if cancel():
                    raise Cancelled
                time.sleep(0.05)
            result["status"] = "SUCCEEDED"
        except Cancelled:
            result["status"] = "CANCELLED"
        except Deadline:
            result.update(status="TIMED_OUT", error="SIPp exceeded the trial deadline")
        except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
            result.update(status="FAILED", error=str(exc))
        finally:
            stop(sipp, signal.SIGINT)
            for proc in captures:
                stop(proc, signal.SIGINT)
            for name in ("qdisc", "sockets", "channels"):
                try:
                    evidence = invoke(name, timeout=4, check=False)
                    if evidence.returncode == 0:
                        if name == "qdisc":
                            qdisc = json.loads(evidence.stdout)
                            storage.json_write(destination / "qdisc.json", qdisc)
                        else:
                            storage.atomic(destination / f"{name}.log", evidence.stdout)
                            if name == "channels" and not evidence.stderr.strip():
                                lines = evidence.stdout.splitlines()
                                if all("!" in line for line in lines if line.strip()):
                                    channel_count = sum("!" in line for line in lines)
                    else:
                        storage.atomic(destination / f"{name}-error.log", evidence.stderr)
                except (OSError, ValueError, subprocess.SubprocessError) as exc:
                    result.setdefault("evidence_errors", []).append(f"{name}: {exc}")
            stop(observer)
            stop(pbx)
            result["cleanup"] = cleanup()
            if not result["cleanup"]["verified"]:
                result["status"] = "CLEANUP_FAILED"
    transfer_logs(destination)
    if samples:
        storage.json_write(destination / "resources.json", samples)
    result["metrics"] = metrics.sipp_metrics(destination, stage.load)
    try:
        pbx_values, events = metrics.pbx_metrics(destination, trial_id)
        result["metrics"].update(pbx_values)
        storage.json_write(destination / "events.json", events)
        pcap, streams = metrics.pcap_metrics(destination)
        result["metrics"].update(pcap)
        storage.json_write(destination / "rtp.json", streams)
    except (OSError, ValueError) as exc:
        result.setdefault("evidence_errors", []).append(str(exc))
    result["metrics"].update(metrics.qdisc_metrics(qdisc))
    result["metrics"].update(metrics.resources(samples))
    result["metrics"]["asterisk_channels_remaining"] = record(
        channel_count, "count", "asterisk_cli", "pbx_channel")

    attempts = result["metrics"]["call_attempts"]["value"]
    success = result["metrics"]["successful_calls"]["value"]
    failures = result["metrics"]["failed_calls"]["value"]
    if result["status"] == "SUCCEEDED" and (
        attempts != stage.load.calls or success is None or failures is None or success + failures != attempts
    ):
        result.update(status="FAILED", error="SIPp final counters are unavailable or incomplete")
    storage.json_write(destination / "result.json", result)


@contextmanager
def signal_flag():
    requested = {"value": False}

    def handler(_signal, _frame):
        requested["value"] = True

    saved = {sig: signal.signal(sig, handler) for sig in (signal.SIGTERM, signal.SIGINT)}
    try:
        yield lambda: requested["value"]
    finally:
        for sig, old in saved.items():
            signal.signal(sig, old)


def status(path, state, **extra):
    data = {"run_id": path.name, "status": state, "updated_at": storage.now(), **extra}
    storage.json_write(path / "status.json", data)
    return data


def recover(root):
    proof = cleanup()
    if not proof["verified"]:
        return proof
    recovered = []
    engine = os.getenv("CALLPATH_ENGINE_ID")
    active = os.environ.get("CALLPATH_EXISTING_CONTAINERS")
    for path in sorted(root.iterdir()):
        if not storage.ID.fullmatch(path.name) or path.is_symlink():
            continue
        file = path / "status.json"
        if not file.is_file():
            continue
        old = storage.json_read(file)
        if old["status"] not in TERMINAL:
            original = old.get("container")
            container_removed = (
                engine and old.get("engine_id") == engine and active is not None
                and original == f"callpath-{path.name}" and original not in active.split()
            )
            verified = original == platform.node() or container_removed
            if verified:
                state = "CANCELLED"
                message = "Interrupted controller; its lab teardown was verified"
            else:
                state = "CLEANUP_FAILED"
                message = "Interrupted controller; previous container teardown is unverified"
            evidence = {"verified": verified, "container": original,
                        "engine_id": old.get("engine_id"), "message": message,
                        "remaining": [] if verified else None}
            storage.json_write(path / "recovery.json", evidence)
            trials = [storage.json_read(trial) for trial in sorted(path.glob("*/result.json"))
                      if not trial.is_symlink() and not trial.parent.is_symlink()]
            if (path / "snapshot.json").is_file():
                summarize(path, trials, evidence, state)
            storage.json_write(path / "artifacts.json", storage.manifest(path))
            recovered.append(status(path, state, error=message, container=original,
                                    engine_id=old.get("engine_id"), created_at=old.get("created_at")))
    return {**proof, "recovered": recovered}


def doctor(profile):
    capabilities()
    tools = toolchain()
    initial = cleanup()
    if not initial["verified"]:
        return {"ok": False, "tools": tools, "cleanup": initial}
    error = None
    try:
        invoke("setup", payload=asdict(profile), timeout=60)
        qdiscs = json.loads(invoke("qdisc").stdout)
        if not any(item.get("kind") == "netem" for entries in qdiscs.values() for item in entries):
            raise RuntimeError("tc did not report a netem queue")
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
        error = str(exc)
    finally:
        proof = cleanup()
    return {"ok": not error and proof["verified"], "tools": tools, "cleanup": proof, "error": error}


def experiment(root, scenario, stages, profile, repeats, run_id=None):
    capabilities()
    with storage.lock(root), signal_flag() as stop_requested:
        recovery = recover(root)
        if not recovery["verified"]:
            raise RuntimeError(f"startup cleanup failed: {recovery}")
        tools = toolchain()
        path = root / (run_id or uuid.uuid4().hex)
        path.mkdir(mode=0o700)
        storage.immutable(path / "snapshot.json",
                          snapshot(path.name, scenario, stages, profile, repeats, tools))
        start_time = storage.now()
        identity = {"created_at": start_time, "container": platform.node(),
                    "engine_id": os.environ.get("CALLPATH_ENGINE_ID")}
        status(path, "QUEUED", **identity, completed_trials=0)
        print(f"Run {path.name}", flush=True)
        trials = []
        state = "SUCCEEDED"

        def cancel():
            return stop_requested() or (path / ".cancel").exists()

        try:
            conditions = (("baseline", profile.baseline()),)
            if profile.impaired:
                conditions += (("impaired", profile),)
            for condition, shaping in conditions:
                if state != "SUCCEEDED":
                    break
                for stage in stages:
                    if state != "SUCCEEDED":
                        break
                    for iteration in range(1, repeats + 1):
                        if cancel():
                            state = "CANCELLED"
                            break
                        name = f"{condition}-{stage.label}-{iteration:02d}"
                        print(name, flush=True)
                        status(path, "RUNNING", **identity,
                               current_trial=name, completed_trials=len(trials))
                        entry = {"directory": name, "condition": condition, "stage": stage.label,
                                 "iteration": iteration, "status": "QUEUED"}
                        trials.append(entry)
                        trial(path / name, stage, shaping, cancel, entry)
                        if entry["status"] != "SUCCEEDED":
                            state = entry["status"]
                            break
        finally:
            if sys.exc_info()[0] is not None:
                state = "FAILED"
            proof = cleanup()
            if not proof["verified"] or any(t.get("status") == "CLEANUP_FAILED" for t in trials):
                state = "CLEANUP_FAILED"
            elif cancel() and state == "SUCCEEDED":
                state = "CANCELLED"
            try:
                summarize(path, trials, proof, state)
                storage.json_write(path / "artifacts.json", storage.manifest(path))
            except (OSError, ValueError, TypeError):
                if state != "CLEANUP_FAILED":
                    state = "FAILED"
                raise
            finally:
                status(path, state, **identity, completed_trials=len(trials))
        print(f"{state} {path}", flush=True)
        return state
