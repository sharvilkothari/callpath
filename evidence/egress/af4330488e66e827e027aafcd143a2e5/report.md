# CallPath S3 run

Run `af4330488e66e827e027aafcd143a2e5` · **SUCCEEDED** · cleanup verified

Target 10.200.1.3 over UDP · PCMU, 20 ms · 1 planned repeats

Shaping profile `{"burst_end_pct": 25, "burst_start_pct": 0, "delay_ms": 0, "duplicate_pct": 0, "jitter_ms": 0, "loss_pct": 0, "path": "forward", "placement": "egress", "queue_limit": 1000, "reorder_pct": 0, "seed": 42, "traffic": "all"}`

## Results by condition

### baseline / soak

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 14.52 | 14.52 | 14.52–14.52 | — | 1/1 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 217.5 | 217.5 | 217.5–217.5 | — | 1/1 | MiB | procfs |
| call_attempts | 240 | 240 | 240–240 | — | 1/1 | count | sipp_csv |
| call_setup_latency_max_ms | 11 | 11 | 11–11 | — | 1/1 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 3 | 3 | 3–3 | — | 1/1 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 5 | 5 | 5–5 | — | 1/1 | ms | sipp_rtt |
| concurrent_calls_peak | 3 | 3 | 3–3 | — | 1/1 | count | sipp_csv_sampled |
| cps_achieved | 1.982 | 1.982 | 1.982–1.982 | — | 1/1 | calls_per_sec | sipp_csv |
| cps_configured | 2 | 2 | 2–2 | — | 1/1 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 1 | 1 | 1–1 | — | 1/1 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| hangup_causes (16) | 240 | 240 | 240–240 | — | 1/1 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 240 | 240 | 240–240 | — | 1/1 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_ami |
| qdisc_drops | 0 | 0 | 0–0 | — | 1/1 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | — | 1/1 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 0 | 0 | 0–0 | — | 1/1 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 0 | 0 | 0–0 | — | 1/1 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 7.617 | 7.617 | 7.617–7.617 | — | 1/1 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 7.613 | 7.613 | 7.613–7.613 | — | 1/1 | ms | tshark_pcap_rtp |
| rtt_ms | 0.1891 | 0.1891 | 0.1891–0.1891 | — | 1/1 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | — | 1/1 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 240 | 240 | 240–240 | — | 1/1 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 480 | 480 | 480–480 | — | 1/1 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| sipp_cpu_pct_peak | 14.5 | 14.5 | 14.5–14.5 | — | 1/1 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 13.55 | 13.55 | 13.55–13.55 | — | 1/1 | MiB | procfs |
| successful_calls | 240 | 240 | 240–240 | — | 1/1 | count | sipp_csv |

## Baseline comparison

| Stage / metric | Impaired − baseline median | Unit |
| --- | ---: | --- |

## Acceptance

| Check | Observed | Threshold | Result |
| --- | ---: | ---: | --- |
| baseline/soak minimum scenario success | 1 | `>= 0.99` | PASS |
| baseline/soak remaining PBX channels | 0 | `<= 0` | PASS |

## Evidence

- [Run snapshot](snapshot.json)
- [Machine-readable report](report.json)
- [Artifact manifest](artifacts.json)
- [baseline-soak-01](baseline-soak-01/trial.json) · SUCCEEDED

## Interpretation

- Experiments describe the isolated local Asterisk lab. Carrier, production and conversational quality conclusions require separate evidence.
- The seeded netem sequence depends on packet order and the host schedule.
- Qdisc drops may include both configured impairment and queue saturation.
- Setup timings are SIP INVITE to first successful response. Echo RTT requires uniquely matched round-trip payloads.
- RTP loss uses sender-to-receiver identity matching. Jitter is the median of final RFC 3550 estimates across streams.
- CPU utilization is process-based, in units of one logical CPU.
- Fewer than five planned repeats per condition; treat observed spread as preliminary.
