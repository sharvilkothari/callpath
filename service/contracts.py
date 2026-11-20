"""Validated API inputs and CLI translation."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from callpath.model import PROFILES, SCENARIOS, configure

LOAD_KEYS = {"calls", "cps", "concurrency", "hold_ms", "timeout_s"}


class Overrides(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    calls: int | None = None
    cps: int | None = None
    concurrency: int | None = None
    hold_ms: int | None = None
    timeout_s: int | None = None
    delay_ms: int | None = None
    jitter_ms: int | None = None
    loss_pct: float | None = None
    queue_limit: int | None = None
    seed: int | None = None
    path: Literal["forward", "reverse", "both"] | None = None
    traffic: Literal["all", "sip", "rtp"] | None = None
    placement: Literal["egress", "ingress"] | None = None
    burst_start_pct: float | None = None
    burst_end_pct: float | None = None
    reorder_pct: float | None = None
    duplicate_pct: float | None = None


class RunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    scenario_id: str
    target_id: str
    impairment_profile_id: str | None = None
    overrides: Overrides = Field(default_factory=Overrides)
    repeats: int | None = None

    @model_validator(mode="after")
    def bounds(self):
        if (self.scenario_id in SCENARIOS and self.target_id == "ast_local"
                and (self.impairment_profile_id is None or self.impairment_profile_id in PROFILES)):
            overrides = self.overrides.model_dump(exclude_none=True)
            configure(self.scenario_id, {key: val for key, val in overrides.items() if key in LOAD_KEYS},
                      {key: val for key, val in overrides.items() if key not in LOAD_KEYS},
                      self.repeats, self.impairment_profile_id)
        return self

    def lab_arguments(self, run_id):
        args = ["run", self.scenario_id, "--run-id", run_id]
        if self.impairment_profile_id:
            args.extend(("--profile", self.impairment_profile_id))
        if self.repeats is not None:
            args.extend(("--repeats", str(self.repeats)))
        for key, value in self.overrides.model_dump(exclude_none=True).items():
            args.extend(("--" + key.replace("_", "-"), str(value)))
        return args
