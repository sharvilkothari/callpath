# CallPath S4 run

Run `23440a2b7f1fde112849808470c1db61` · **SUCCEEDED** · cleanup verified

Target 10.200.1.3 over UDP · PCMU, 20 ms · 5 planned repeats

Shaping profile `{"burst_end_pct": 25, "burst_start_pct": 0, "delay_ms": 0, "duplicate_pct": 0, "jitter_ms": 0, "loss_pct": 0, "path": "forward", "placement": "egress", "queue_limit": 1000, "reorder_pct": 0, "seed": 42, "traffic": "sip"}`

## Results by condition

### baseline / delay

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 14.99 | 14.54 | 9.516–19.43 | 4.866 | 5/5 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 208.8 | 204.3 | 193.6–209.3 | 7.007 | 5/5 | MiB | procfs |
| call_attempts | 5 | 5 | 5–5 | 0 | 5/5 | count | sipp_csv |
| call_setup_latency_max_ms | 12 | 19.6 | 6–39 | 15.69 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 5 | 4.4 | 2–7 | 2.302 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 12 | 19.6 | 6–39 | 15.69 | 5/5 | ms | sipp_rtt |
| concurrent_calls_peak | 4 | 4 | 4–4 | 0 | 5/5 | count | sipp_csv_sampled |
| cps_achieved | 1.229 | 1.229 | 1.226–1.23 | 0.001673 | 5/5 | calls_per_sec | sipp_csv |
| cps_configured | 2 | 2 | 2–2 | 0 | 5/5 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 1 | 1 | 1–1 | 0 | 5/5 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| hangup_causes (16) | 5 | 5 | 5–5 | 0 | 5/5 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 5 | 5 | 5–5 | 0 | 5/5 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| qdisc_drops | 0 | 0 | 0–0 | 0 | 5/5 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | 0 | 5/5 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 0 | 0 | 0–0 | 0 | 5/5 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 0 | 0 | 0–0 | 0 | 5/5 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 3.15 | 4.056 | 1.892–7.819 | 2.403 | 5/5 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 3.141 | 3.831 | 1.886–7.821 | 2.356 | 5/5 | ms | tshark_pcap_rtp |
| rtt_ms | 0.1242 | 0.1276 | 0.123–0.14 | 0.007047 | 5/5 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | 0 | 5/5 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 5 | 5 | 5–5 | 0 | 5/5 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 10 | 10 | 10–10 | 0 | 5/5 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sipp_cpu_pct_peak | 4.894 | 9.86 | 4.792–24.98 | 8.716 | 5/5 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 13.48 | 13.76 | 13.3–15.01 | 0.7183 | 5/5 | MiB | procfs |
| successful_calls | 5 | 5 | 5–5 | 0 | 5/5 | count | sipp_csv |

## Baseline comparison

| Stage / metric | Impaired − baseline median | Unit |
| --- | ---: | --- |

## Acceptance

| Check | Observed | Threshold | Result |
| --- | ---: | ---: | --- |
| baseline/delay minimum scenario success | 1 | `>= 0.99` | PASS |

## Evidence

- [Run snapshot](snapshot.json)
- [Machine-readable report](report.json)
- [Artifact manifest](artifacts.json)
- [baseline-delay-01](baseline-delay-01/trial.json) · SUCCEEDED
- [baseline-delay-02](baseline-delay-02/trial.json) · SUCCEEDED
- [baseline-delay-03](baseline-delay-03/trial.json) · SUCCEEDED
- [baseline-delay-04](baseline-delay-04/trial.json) · SUCCEEDED
- [baseline-delay-05](baseline-delay-05/trial.json) · SUCCEEDED

## Interpretation

- Experiments describe the isolated local Asterisk lab. Carrier, production and conversational quality conclusions require separate evidence.
- The seeded netem sequence depends on packet order and the host schedule.
- Qdisc drops may include both configured impairment and queue saturation.
- Setup timings are SIP INVITE to first successful response. Echo RTT requires uniquely matched round-trip payloads.
- RTP loss uses sender-to-receiver identity matching. Jitter is the median of final RFC 3550 estimates across streams.
- CPU utilization is process-based, in units of one logical CPU.
