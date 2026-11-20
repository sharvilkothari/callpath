from dataclasses import asdict, dataclass, replace
import math

SIPP_IP = "10.200.1.2"
PBX_IP = "10.200.1.3"
SIP_PORT = 5060
RTP_MIN, RTP_MAX = 10000, 10199
EXTENSION = "7000"
MEDIA = {"codec": "PCMU", "clock_hz": 8000, "ptime_ms": 20,
         "source": "SIPp generated tone; Asterisk Echo", "payload_type": 0}
MAX_TIMEOUT = 900
TERMINAL = {"SUCCEEDED", "FAILED", "TIMED_OUT", "CANCELLED", "CLEANUP_FAILED"}


def bounded(name, value, low, high, kind):
    if isinstance(value, bool) or not isinstance(value, kind):
        raise ValueError(f"{name} must be numeric")
    if not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f"{name} must be in [{low}, {high}]")


@dataclass(frozen=True)
class Profile:
    delay_ms: int = 0
    jitter_ms: int = 0
    loss_pct: float = 0
    queue_limit: int = 1000
    seed: int = 42
    path: str = "forward"
    traffic: str = "all"
    placement: str = "egress"
    burst_start_pct: float = 0
    burst_end_pct: float = 25
    reorder_pct: float = 0
    duplicate_pct: float = 0

    def __post_init__(self):
        for key, lo, hi in (
            ("delay_ms", 0, 2000), ("jitter_ms", 0, self.delay_ms),
            ("queue_limit", 10, 10000), ("seed", 1, 2**32-1),
        ):
            bounded(key, getattr(self, key), lo, hi, int)
        for key, lo, hi in (
            ("loss_pct", 0, 25), ("burst_start_pct", 0, 25),
            ("burst_end_pct", 1, 100), ("reorder_pct", 0, 25),
            ("duplicate_pct", 0, 25),
        ):
            bounded(key, getattr(self, key), lo, hi, (int, float))
        if self.path not in ("forward", "reverse", "both"):
            raise ValueError("path must be forward, reverse or both")
        if self.traffic not in ("all", "sip", "rtp"):
            raise ValueError("traffic must be all, sip or rtp")
        if self.placement not in ("egress", "ingress"):
            raise ValueError("placement must be egress or ingress")
        if self.loss_pct and self.burst_start_pct:
            raise ValueError("choose random or burst loss")
        if self.reorder_pct and not self.delay_ms:
            raise ValueError("reorder requires delay")

    @property
    def impaired(self):
        return bool(self.delay_ms or self.loss_pct or self.burst_start_pct
                    or self.reorder_pct or self.duplicate_pct)

    def baseline(self):
        return replace(self, delay_ms=0, jitter_ms=0, loss_pct=0,
                       burst_start_pct=0, reorder_pct=0, duplicate_pct=0)

    def netem(self):
        args = ["limit", str(self.queue_limit)]
        if self.delay_ms:
            args += ["delay", f"{self.delay_ms}ms"]
            if self.jitter_ms:
                args += [f"{self.jitter_ms}ms", "distribution", "normal"]
        if self.loss_pct:
            args += ["loss", "random", f"{self.loss_pct:g}%"]
        if self.burst_start_pct:
            args += ["loss", "gemodel", f"{self.burst_start_pct:g}%",
                     f"{self.burst_end_pct:g}%", "100%", "0%"]
        if self.reorder_pct:
            args += ["reorder", f"{self.reorder_pct:g}%"]
        if self.duplicate_pct:
            args += ["duplicate", f"{self.duplicate_pct:g}%"]
        if self.impaired:
            args += ["seed", str(self.seed)]
        return args


@dataclass(frozen=True)
class Load:
    calls: int
    cps: int
    concurrency: int
    hold_ms: int
    timeout_s: int

    def __post_init__(self):
        for key, lo, hi in (
            ("calls", 1, 1500), ("cps", 1, 20), ("concurrency", 1, 40),
            ("hold_ms", 300, 8000), ("timeout_s", 2, MAX_TIMEOUT),
        ):
            bounded(key, getattr(self, key), lo, hi, int)


@dataclass(frozen=True)
class Stage:
    load: Load
    label: str


def plan(scenario, overrides):
    defaults = {
        "S0": [Stage(Load(1, 1, 1, 1000, 25), "smoke")],
        "S1": [Stage(Load(10, 2, 4, 1000, 35), "baseline")],
        "S2": [Stage(Load(cps * 6, cps, active, 2000, 55), f"ramp-{cps}")
               for cps, active in ((2, 5), (5, 12), (10, 24))],
        "S3": [Stage(Load(240, 2, 5, 1000, 180), "soak")],
        "S4": [Stage(Load(10, 2, 6, 1500, 45), "delay")],
        "S5": [Stage(Load(10, 2, 6, 1500, 45), "loss")],
        "S6": [Stage(Load(5, 1, 2, 1200, 45), "dtmf"),
               Stage(Load(5, 1, 2, 1200, 45), "transfer")],
        "S7": [Stage(Load(10, 2, 6, 2000, 45), "echo")],
    }
    return [replace(stage, load=replace(stage.load, **overrides)) for stage in defaults[scenario]]


def record(value, unit, source, direction, reason=None):
    result = {"value": value, "unit": unit, "source": source, "direction": direction,
              "availability": "available" if value is not None else "unavailable"}
    if value is None:
        result["reason"] = reason or "No valid samples collected"
    return result

SCENARIOS = {
    "S0": "Smoke call", "S1": "Repeated baseline", "S2": "Concurrency ramp",
    "S3": "Soak", "S4": "Delay and jitter", "S5": "Packet loss",
    "S6": "DTMF and transfer", "S7": "RTP echo",
}

PROFILES = {
    "baseline": {},
    "delay": {"delay_ms": 80, "jitter_ms": 20},
    "loss": {"loss_pct": 1},
    "burst": {"burst_start_pct": 1, "burst_end_pct": 25},
    "echo": {"delay_ms": 40, "jitter_ms": 10, "traffic": "rtp", "path": "both"},
}


def configure(scenario, load_overrides, profile_overrides, repeats=None, profile_id=None,
              baseline_only=False):
    default_id = {"S4": "delay", "S5": "loss", "S7": "echo"}.get(scenario, "baseline")
    defaults = dict(PROFILES[profile_id or default_id])
    if profile_overrides.get("burst_start_pct") and "loss_pct" not in profile_overrides:
        defaults["loss_pct"] = 0
    profile = Profile(**(defaults | profile_overrides))
    if baseline_only:
        profile = profile.baseline()
    if repeats is None:
        repeats = 5 if scenario in ("S1", "S4", "S5", "S7") else 1
    bounded("repeats", repeats, 1, 15, int)
    return plan(scenario, load_overrides), profile, repeats
