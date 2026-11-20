"""Privileged, fixed-command broker. Install this tree read-only to the runner."""
import argparse
from dataclasses import asdict
import json
from ipaddress import IPv4Address, summarize_address_range
import os
from pathlib import Path
import pwd
import signal
import subprocess
import sys
import time

ROOT = Path("/opt/callpath")
sys.path.insert(0, str(ROOT))
from callpath.model import PBX_IP, RTP_MAX, RTP_MIN, SIPP_IP, Load, Profile  # noqa: E402

IP = "/usr/sbin/ip"
TC = "/usr/sbin/tc"
PBX = "/usr/sbin/asterisk"
WORK = Path("/run/callpath-work")
OWNER = Path("/run/callpath-helper/lease")
NS = {"sipp": "cp-sipp", "pbx": "cp-pbx"}
IFACE = {"sipp": "cp-veth-sipp", "pbx": "cp-veth-pbx"}
TAP_IN, TAP_OUT, IFB = "cp-tap-in", "cp-tap-out", "cp-ifb"
HOSTS = {"sipp": SIPP_IP, "pbx": PBX_IP}
ENV = {"PATH": "/usr/sbin:/usr/bin:/sbin:/bin", "LC_ALL": "C.UTF-8",
       "HOME": str(WORK), "TERM": "dumb"}
CONFIG = str(ROOT / "asterisk/asterisk.conf")
SCENARIOS = {"call": ("call.xml", "7000"), "dtmf": ("dtmf.xml", "7001"),
             "transfer": ("transfer.xml", "7002")}


def cmd(*argv, timeout=8):
    proc = subprocess.run(argv, text=True, capture_output=True, env=ENV, timeout=timeout)
    if proc.returncode:
        raise RuntimeError(f"{' '.join(argv[:8])}: {proc.stderr.strip()}")
    return proc.stdout


def net(side, *argv):
    return cmd(IP, "netns", "exec", NS[side], *argv)


def namespaces():
    return {line.split()[0] for line in cmd(IP, "netns", "list").splitlines() if line}


def host_links():
    return {item["ifname"] for item in json.loads(cmd(IP, "-j", "link", "show"))}


def ingress_sides(profile):
    if profile.placement != "ingress":
        return ()
    return tuple(side for side, path in (("pbx", "forward"), ("sipp", "reverse"))
                 if profile.path in (path, "both"))


def shape(side, device, path, profile):
    qdisc = (TC, "qdisc", "add", "dev", device)
    if profile.traffic == "all":
        net(side, *qdisc, "root", "handle", "10:", "netem", *profile.netem())
        return
    net(side, *qdisc, "root", "handle", "1:", "prio", "bands", "2", "priomap", *(["0"] * 16))
    net(side, *qdisc, "parent", "1:2", "handle", "10:", "netem", *profile.netem())
    port_key = "dport" if path == "forward" or profile.traffic == "sip" else "sport"
    ranges = ((5060, 0xffff),) if profile.traffic == "sip" else (
        (int(mask.network_address), int(mask.netmask) & 0xffff)
        for mask in summarize_address_range(IPv4Address(RTP_MIN), IPv4Address(RTP_MAX)))
    for port, mask in ranges:
        net(side, TC, "filter", "add", "dev", device, "parent", "1:", "protocol",
            "ip", "prio", "10", "u32", "match", "ip", "protocol", "17", "0xff",
            "match", "ip", port_key, str(port), hex(mask), "flowid", "1:2")


def setup(profile):
    if OWNER.exists():
        raise RuntimeError("stale lease; run cleanup first")
    if namespaces() & set(NS.values()) or host_links() & set(IFACE.values()):
        raise RuntimeError("namespace or veth name collision")
    with OWNER.open("x") as lease:
        json.dump(asdict(profile), lease)
    for side in NS:
        cmd(IP, "netns", "add", NS[side])
    cmd(IP, "link", "add", IFACE["sipp"], "type", "veth", "peer", "name", IFACE["pbx"])
    for side, interface in IFACE.items():
        cmd(IP, "link", "set", interface, "netns", NS[side])
        net(side, IP, "link", "set", "lo", "up")
        net(side, IP, "addr", "add", HOSTS[side] + "/24", "dev", interface)
        net(side, IP, "link", "set", interface, "up")
        net(side, IP, "link", "add", TAP_OUT, "type", "veth", "peer", "name", TAP_IN)
        for tap in (TAP_OUT, TAP_IN):
            net(side, IP, "link", "set", tap, "up")
        net(side, TC, "qdisc", "add", "dev", interface, "clsact")
        net(side, TC, "filter", "add", "dev", interface, "egress", "protocol",
            "ip", "matchall", "action", "mirred", "egress", "mirror", "dev", TAP_OUT)
        if any(route.get("dst") == "default" for route in
               json.loads(net(side, IP, "-j", "route", "show"))):
            raise RuntimeError("unexpected default route in isolated namespace")
    for sender, receiver, path in (("sipp", "pbx", "forward"), ("pbx", "sipp", "reverse")):
        if profile.path not in (path, "both"):
            continue
        if profile.placement == "egress":
            shape(sender, IFACE[sender], path, profile)
        else:
            net(receiver, IP, "link", "add", IFB, "type", "ifb")
            net(receiver, IP, "link", "set", IFB, "up")
            net(receiver, TC, "filter", "add", "dev", IFACE[receiver], "ingress",
                "protocol", "ip", "matchall", "action", "mirred", "egress", "redirect", "dev", IFB)
            shape(receiver, IFB, path, profile)


def pids(name):
    return {int(pid) for pid in cmd(IP, "netns", "pids", name).split()}


def cleanup():
    owned = OWNER.exists()
    errors = []
    if owned:
        for name in sorted(namespaces() & set(NS.values())):
            for sig, wait in ((signal.SIGTERM, 1), (signal.SIGKILL, 2)):
                for pid in pids(name):
                    try:
                        os.kill(pid, sig)
                    except ProcessLookupError:
                        pass
                deadline = time.monotonic() + wait
                while pids(name) and time.monotonic() < deadline:
                    time.sleep(0.05)
            if pids(name):
                errors.append(f"{name} still contains processes")
                continue
            try:
                cmd(IP, "netns", "del", name)
            except RuntimeError as exc:
                errors.append(str(exc))
        for interface in sorted(host_links() & set(IFACE.values())):
            try:
                cmd(IP, "link", "del", interface)
            except RuntimeError as exc:
                if interface in host_links():
                    errors.append(str(exc))
    remaining = sorted((namespaces() & set(NS.values())) | (host_links() & set(IFACE.values())))
    verified = not errors and not remaining
    if owned and verified:
        OWNER.unlink()
    print(json.dumps({"verified": verified, "remaining": remaining, "errors": errors}))
    return 0 if verified else 1


def worker(side, user, *argv):
    os.execve(IP, (IP, "netns", "exec", NS[side], "/usr/bin/setpriv",
                   "--reuid", str(user.pw_uid), "--regid", str(user.pw_gid),
                   "--clear-groups", "--no-new-privs", *argv), ENV)


def request():
    payload = sys.stdin.buffer.read(8193)
    if len(payload) > 8192:
        raise ValueError("payload too large")
    obj = json.loads(payload)
    if not isinstance(obj, dict):
        raise ValueError("expected object")
    return obj


def main():
    if os.geteuid() != 0 or os.environ.get("SUDO_USER") != "callpath":
        raise ValueError("helper requires the dedicated runner account")
    user = pwd.getpwnam("callpath")
    if user.pw_uid < 1 or user.pw_uid != int(os.environ["SUDO_UID"]):
        raise ValueError("invalid caller uid")
    os.chdir("/")
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest="op", required=True)
    for op in ("setup", "cleanup", "qdisc", "pbx", "ready", "channels", "ami", "sipp", "sockets"):
        subs.add_parser(op)
    capture = subs.add_parser("capture")
    capture.add_argument("side", choices=NS)
    capture.add_argument("direction", choices=("tx", "rx"))
    args = parser.parse_args()
    if args.op == "setup":
        setup(Profile(**request()))
        return 0
    if args.op == "cleanup":
        return cleanup()
    if not OWNER.is_file():
        raise RuntimeError("no configured lab")
    profile = Profile(**json.loads(OWNER.read_text()))
    if args.op == "qdisc":
        devices = {side: [interface] for side, interface in IFACE.items()}
        for side in ingress_sides(profile):
            devices[side].append(IFB)
        print(json.dumps({f"{side}/{dev}": json.loads(net(
            side, TC, "-s", "-j", "qdisc", "show", "dev", dev))
            for side, links in devices.items() for dev in links}))
    elif args.op == "sockets":
        print(json.dumps({side: net(side, "/usr/bin/ss", "-H", "-uan") for side in NS}))
    elif args.op == "pbx":
        worker("pbx", user, PBX, "-C", CONFIG, "-f", "-g", "-n")
    elif args.op in ("ready", "channels"):
        command = "core waitfullybooted" if args.op == "ready" else "core show channels concise"
        worker("pbx", user, PBX, "-C", CONFIG, "-rx", command)
    elif args.op == "ami":
        worker("pbx", user, "/usr/bin/python3", "-I", str(ROOT / "network/ami.py"))
    elif args.op == "capture":
        side, direction = args.side, args.direction
        interface = IFB if side in ingress_sides(profile) else IFACE[side]
        if direction == "tx":
            interface = TAP_IN
        owner_peer = PBX_IP if side == "sipp" else SIPP_IP
        src, dst = (HOSTS[side], owner_peer) if direction == "tx" else (owner_peer, HOSTS[side])
        os.execve(IP, (IP, "netns", "exec", NS[side], "/usr/bin/tcpdump", "-Z", user.pw_name,
                       "-i", interface, "-B", "4096", "--immediate-mode", "-U", "-s", "1024", "-w", "-",
                       "udp", "and", "src", "host", src, "and", "dst", "host", dst), ENV)
    elif args.op == "sipp":
        data = request()
        scenario, extension = SCENARIOS[data.pop("flow")]
        run_id = data.pop("run_id")
        if not isinstance(run_id, str) or len(run_id) != 32 or any(c not in "0123456789abcdef" for c in run_id):
            raise ValueError("invalid trial id")
        load = Load(**data)
        worker("sipp", user, "/usr/bin/python3", "-I", str(ROOT / "network/sipp_worker.py"),
               scenario, extension, run_id, str(load.calls), str(load.cps),
               str(load.concurrency), str(load.hold_ms))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print(f"callpath-helper: {exc}", file=sys.stderr)
        sys.exit(1)
