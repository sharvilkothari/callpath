# CallPath S3 run

Run `45a31abd50dd4726a0eda962d8405f38` · **CANCELLED** · cleanup verified

Target 10.200.1.3 over UDP · PCMU, 20 ms · 1 planned repeats

Shaping profile `{"burst_end_pct": 25, "burst_start_pct": 0, "delay_ms": 0, "duplicate_pct": 0, "jitter_ms": 0, "loss_pct": 0, "path": "forward", "placement": "egress", "queue_limit": 1000, "reorder_pct": 0, "seed": 42, "traffic": "all"}`

## Results by condition

### baseline / soak

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |

## Baseline comparison

| Stage / metric | Impaired − baseline median | Unit |
| --- | ---: | --- |

## Acceptance

| Check | Observed | Threshold | Result |
| --- | ---: | ---: | --- |
| baseline/soak minimum scenario success | — | `>= 0.99` | INSUFFICIENT_EVIDENCE |
| baseline/soak remaining PBX channels | — | `<= 0` | INSUFFICIENT_EVIDENCE |

## Evidence

- [Run snapshot](snapshot.json)
- [Machine-readable report](report.json)
- [Artifact manifest](artifacts.json)
- [baseline-soak-01](baseline-soak-01/trial.json) · CANCELLED

## Interpretation

- Experiments describe the isolated local Asterisk lab. Carrier, production and conversational quality conclusions require separate evidence.
- The seeded netem sequence depends on packet order and the host schedule.
- Qdisc drops may include both configured impairment and queue saturation.
- Setup timings are SIP INVITE to first successful response. Echo RTT requires uniquely matched round-trip payloads.
- RTP loss uses sender-to-receiver identity matching. Jitter is the median of final RFC 3550 estimates across streams.
- CPU utilization is process-based, in units of one logical CPU.
- Fewer than five planned repeats per condition; treat observed spread as preliminary.
