# CallPath S0 run

Run `46c8c5936e59413ea89acc4dbaff12ad` · **SUCCEEDED** · cleanup verified

Target 10.200.1.3 over UDP · PCMU, 20 ms · 1 planned repeats

Shaping profile `{"burst_end_pct": 25, "burst_start_pct": 0, "delay_ms": 0, "duplicate_pct": 0, "jitter_ms": 0, "loss_pct": 0, "path": "forward", "placement": "egress", "queue_limit": 1000, "reorder_pct": 0, "seed": 42, "traffic": "all"}`

## Results by condition

### baseline / smoke

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 4.815 | 4.815 | 4.815–4.815 | — | 1/1 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 202.7 | 202.7 | 202.7–202.7 | — | 1/1 | MiB | procfs |
| call_attempts | 1 | 1 | 1–1 | — | 1/1 | count | sipp_csv |
| call_setup_latency_max_ms | 6 | 6 | 6–6 | — | 1/1 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 6 | 6 | 6–6 | — | 1/1 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 6 | 6 | 6–6 | — | 1/1 | ms | sipp_rtt |
| concurrent_calls_peak | 1 | 1 | 1–1 | — | 1/1 | count | sipp_csv_sampled |
| cps_achieved | 0.482 | 0.482 | 0.482–0.482 | — | 1/1 | calls_per_sec | sipp_csv |
| cps_configured | 1 | 1 | 1–1 | — | 1/1 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 1 | 1 | 1–1 | — | 1/1 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| hangup_causes (16) | 1 | 1 | 1–1 | — | 1/1 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 1 | 1 | 1–1 | — | 1/1 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_ami |
| qdisc_drops | 0 | 0 | 0–0 | — | 1/1 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | — | 1/1 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 0 | 0 | 0–0 | — | 1/1 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 0 | 0 | 0–0 | — | 1/1 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 4.087 | 4.087 | 4.087–4.087 | — | 1/1 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 4.079 | 4.079 | 4.079–4.079 | — | 1/1 | ms | tshark_pcap_rtp |
| rtt_ms | 0.2429 | 0.2429 | 0.2429–0.2429 | — | 1/1 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | — | 1/1 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 1 | 1 | 1–1 | — | 1/1 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 2 | 2 | 2–2 | — | 1/1 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| sipp_cpu_pct_peak | 4.81 | 4.81 | 4.81–4.81 | — | 1/1 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 13.35 | 13.35 | 13.35–13.35 | — | 1/1 | MiB | procfs |
| successful_calls | 1 | 1 | 1–1 | — | 1/1 | count | sipp_csv |

## Baseline comparison

| Stage / metric | Impaired − baseline median | Unit |
| --- | ---: | --- |

## Acceptance

| Check | Observed | Threshold | Result |
| --- | ---: | ---: | --- |
| baseline/smoke minimum scenario success | 1 | `>= 0.99` | PASS |
| baseline/smoke correlated PBX calls | 1 | `>= 1` | PASS |

## Evidence

- [Run snapshot](snapshot.json)
- [Machine-readable report](report.json)
- [Artifact manifest](artifacts.json)
- [baseline-smoke-01](baseline-smoke-01/trial.json) · SUCCEEDED

## Interpretation

- Experiments describe the isolated local Asterisk lab. Carrier, production and conversational quality conclusions require separate evidence.
- The seeded netem sequence depends on packet order and the host schedule.
- Qdisc drops may include both configured impairment and queue saturation.
- Setup timings are SIP INVITE to first successful response. Echo RTT requires uniquely matched round-trip payloads.
- RTP loss uses sender-to-receiver identity matching. Jitter is the median of final RFC 3550 estimates across streams.
- CPU utilization is process-based, in units of one logical CPU.
- Fewer than five planned repeats per condition; treat observed spread as preliminary.
