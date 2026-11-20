# CallPath S1 run

Run `72142963545ae7f5e32923f541c1db91` · **SUCCEEDED** · cleanup verified

Target 10.200.1.3 over UDP · PCMU, 20 ms · 5 planned repeats

Shaping profile `{"burst_end_pct": 25, "burst_start_pct": 0, "delay_ms": 0, "duplicate_pct": 0, "jitter_ms": 0, "loss_pct": 0, "path": "forward", "placement": "egress", "queue_limit": 1000, "reorder_pct": 0, "seed": 42, "traffic": "all"}`

## Results by condition

### baseline / baseline

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 9.47 | 9.257 | 8.669–9.649 | 0.4021 | 5/5 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 206.9 | 206.1 | 204.6–207 | 1.136 | 5/5 | MiB | procfs |
| call_attempts | 10 | 10 | 10–10 | 0 | 5/5 | count | sipp_csv |
| call_setup_latency_max_ms | 7 | 6.6 | 5–8 | 1.14 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 3 | 3 | 3–3 | 0 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 7 | 6.6 | 5–8 | 1.14 | 5/5 | ms | sipp_rtt |
| concurrent_calls_peak | 3 | 3 | 3–3 | 0 | 5/5 | count | sipp_csv_sampled |
| cps_achieved | 1.646 | 1.647 | 1.645–1.649 | 0.001817 | 5/5 | calls_per_sec | sipp_csv |
| cps_configured | 2 | 2 | 2–2 | 0 | 5/5 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 1 | 1 | 1–1 | 0 | 5/5 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| hangup_causes (16) | 10 | 10 | 10–10 | 0 | 5/5 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 10 | 10 | 10–10 | 0 | 5/5 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| qdisc_drops | 0 | 0 | 0–0 | 0 | 5/5 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | 0 | 5/5 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 0 | 0 | 0–0 | 0 | 5/5 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 0 | 0 | 0–0 | 0 | 5/5 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 7.085 | 7.018 | 5.644–8.112 | 1.064 | 5/5 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 7.076 | 7.003 | 5.623–8.115 | 1.08 | 5/5 | ms | tshark_pcap_rtp |
| rtt_ms | 0.2179 | 0.2054 | 0.1671–0.2339 | 0.02687 | 5/5 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | 0 | 5/5 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 10 | 10 | 10–10 | 0 | 5/5 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 20 | 20 | 20–20 | 0 | 5/5 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sipp_cpu_pct_peak | 9.006 | 7.479 | 4.755–9.455 | 2.484 | 5/5 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 13.68 | 14.22 | 13.29–15.41 | 1.045 | 5/5 | MiB | procfs |
| successful_calls | 10 | 10 | 10–10 | 0 | 5/5 | count | sipp_csv |

## Baseline comparison

| Stage / metric | Impaired − baseline median | Unit |
| --- | ---: | --- |

## Acceptance

| Check | Observed | Threshold | Result |
| --- | ---: | ---: | --- |
| baseline/baseline minimum scenario success | 1 | `>= 0.99` | PASS |
| baseline/baseline setup p95 spread (ms) | 3 | `<= 40` | PASS |

## Evidence

- [Run snapshot](snapshot.json)
- [Machine-readable report](report.json)
- [Artifact manifest](artifacts.json)
- [baseline-baseline-01](baseline-baseline-01/trial.json) · SUCCEEDED
- [baseline-baseline-02](baseline-baseline-02/trial.json) · SUCCEEDED
- [baseline-baseline-03](baseline-baseline-03/trial.json) · SUCCEEDED
- [baseline-baseline-04](baseline-baseline-04/trial.json) · SUCCEEDED
- [baseline-baseline-05](baseline-baseline-05/trial.json) · SUCCEEDED

## Interpretation

- Experiments describe the isolated local Asterisk lab. Carrier, production and conversational quality conclusions require separate evidence.
- The seeded netem sequence depends on packet order and the host schedule.
- Qdisc drops may include both configured impairment and queue saturation.
- Setup timings are SIP INVITE to first successful response. Echo RTT requires uniquely matched round-trip payloads.
- RTP loss uses sender-to-receiver identity matching. Jitter is the median of final RFC 3550 estimates across streams.
- CPU utilization is process-based, in units of one logical CPU.
