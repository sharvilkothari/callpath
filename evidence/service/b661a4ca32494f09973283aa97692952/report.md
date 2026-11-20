# CallPath S4 run

Run `b661a4ca32494f09973283aa97692952` · **SUCCEEDED** · cleanup verified

Target 10.200.1.3 over UDP · PCMU, 20 ms · 1 planned repeats

Shaping profile `{"burst_end_pct": 25, "burst_start_pct": 0, "delay_ms": 80, "duplicate_pct": 0, "jitter_ms": 20, "loss_pct": 0, "path": "forward", "placement": "egress", "queue_limit": 1000, "reorder_pct": 0, "seed": 42, "traffic": "all"}`

## Results by condition

### baseline / delay

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 9.631 | 9.631 | 9.631–9.631 | — | 1/1 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 179.1 | 179.1 | 179.1–179.1 | — | 1/1 | MiB | procfs |
| call_attempts | 3 | 3 | 3–3 | — | 1/1 | count | sipp_csv |
| call_setup_latency_max_ms | 9 | 9 | 9–9 | — | 1/1 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 7 | 7 | 7–7 | — | 1/1 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 9 | 9 | 9–9 | — | 1/1 | ms | sipp_rtt |
| concurrent_calls_peak | 3 | 3 | 3–3 | — | 1/1 | count | sipp_csv_sampled |
| cps_achieved | 0.977 | 0.977 | 0.977–0.977 | — | 1/1 | calls_per_sec | sipp_csv |
| cps_configured | 2 | 2 | 2–2 | — | 1/1 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 0.9954 | 0.9954 | 0.9954–0.9954 | — | 1/1 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| hangup_causes (16) | 3 | 3 | 3–3 | — | 1/1 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 3 | 3 | 3–3 | — | 1/1 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_ami |
| qdisc_drops | 0 | 0 | 0–0 | — | 1/1 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | — | 1/1 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 0 | 0 | 0–0 | — | 1/1 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 0 | 0 | 0–0 | — | 1/1 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 1.296 | 1.296 | 1.296–1.296 | — | 1/1 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 1.234 | 1.234 | 1.234–1.234 | — | 1/1 | ms | tshark_pcap_rtp |
| rtt_ms | 0.175 | 0.175 | 0.175–0.175 | — | 1/1 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | — | 1/1 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 3 | 3 | 3–3 | — | 1/1 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 6 | 6 | 6–6 | — | 1/1 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| sipp_cpu_pct_peak | 4.815 | 4.815 | 4.815–4.815 | — | 1/1 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 11.3 | 11.3 | 11.3–11.3 | — | 1/1 | MiB | procfs |
| successful_calls | 3 | 3 | 3–3 | — | 1/1 | count | sipp_csv |

### impaired / delay

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 9.489 | 9.489 | 9.489–9.489 | — | 1/1 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 188.8 | 188.8 | 188.8–188.8 | — | 1/1 | MiB | procfs |
| call_attempts | 3 | 3 | 3–3 | — | 1/1 | count | sipp_csv |
| call_setup_latency_max_ms | 210 | 210 | 210–210 | — | 1/1 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 121 | 121 | 121–121 | — | 1/1 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 210 | 210 | 210–210 | — | 1/1 | ms | sipp_rtt |
| concurrent_calls_peak | 3 | 3 | 3–3 | — | 1/1 | count | sipp_csv_sampled |
| cps_achieved | 0.916 | 0.916 | 0.916–0.916 | — | 1/1 | calls_per_sec | sipp_csv |
| cps_configured | 2 | 2 | 2–2 | — | 1/1 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 0.9437 | 0.9437 | 0.9437–0.9437 | — | 1/1 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| hangup_causes (16) | 3 | 3 | 3–3 | — | 1/1 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 3 | 3 | 3–3 | — | 1/1 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_ami |
| qdisc_drops | 0 | 0 | 0–0 | — | 1/1 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | — | 1/1 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 0 | 0 | 0–0 | — | 1/1 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 0 | 0 | 0–0 | — | 1/1 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 29.09 | 29.09 | 29.09–29.09 | — | 1/1 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 28.39 | 28.39 | 28.39–28.39 | — | 1/1 | ms | tshark_pcap_rtp |
| rtt_ms | 79.32 | 79.32 | 79.32–79.32 | — | 1/1 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | — | 1/1 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 3 | 3 | 3–3 | — | 1/1 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 6 | 6 | 6–6 | — | 1/1 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| sipp_cpu_pct_peak | 4.756 | 4.756 | 4.756–4.756 | — | 1/1 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 15.17 | 15.17 | 15.17–15.17 | — | 1/1 | MiB | procfs |
| successful_calls | 3 | 3 | 3–3 | — | 1/1 | count | sipp_csv |

## Baseline comparison

| Stage / metric | Impaired − baseline median | Unit |
| --- | ---: | --- |
| delay/asterisk_channels_remaining | 0 | count |
| delay/asterisk_cpu_pct_peak | -0.1415 | pct_one_logical_cpu |
| delay/asterisk_rss_mib_peak | 9.73 | MiB |
| delay/call_attempts | 0 | count |
| delay/call_setup_latency_max_ms | 201 | ms |
| delay/call_setup_latency_p50_ms | 114 | ms |
| delay/call_setup_latency_p95_ms | 201 | ms |
| delay/concurrent_calls_peak | 0 | count |
| delay/cps_achieved | -0.061 | calls_per_sec |
| delay/cps_configured | 0 | calls_per_sec |
| delay/echo_unique_payload_match_rate | -0.05171 | ratio |
| delay/failed_calls | 0 | count |
| delay/pbx_call_ids_correlated | 0 | count |
| delay/pbx_dtmf_confirmed | 0 | count |
| delay/pbx_transfer_confirmed | 0 | count |
| delay/qdisc_drops | 0 | count |
| delay/qdisc_overlimits | 0 | count |
| delay/rtp_packet_loss_pbx_to_uac | 0 | pct |
| delay/rtp_packet_loss_uac_to_pbx | 0 | pct |
| delay/rtp_receiver_jitter_pbx_to_uac | 27.8 | ms |
| delay/rtp_receiver_jitter_uac_to_pbx | 27.15 | ms |
| delay/rtt_ms | 79.15 | ms |
| delay/scenario_success_rate | 0 | ratio |
| delay/sip_retransmits | 0 | count |
| delay/sip_timeouts | 0 | count |
| delay/sipp_cpu_pct_peak | -0.05927 | pct_one_logical_cpu |
| delay/sipp_rss_mib_peak | 3.867 | MiB |
| delay/successful_calls | 0 | count |

## Acceptance

| Check | Observed | Threshold | Result |
| --- | ---: | ---: | --- |
| baseline/delay minimum scenario success | 1 | `>= 0.99` | PASS |
| impaired/delay minimum scenario success | 1 | `>= 0.95` | PASS |
| impaired/delay median setup p95 delta (ms) | 201 | `<= 240` | PASS |

## Evidence

- [Run snapshot](snapshot.json)
- [Machine-readable report](report.json)
- [Artifact manifest](artifacts.json)
- [baseline-delay-01](baseline-delay-01/trial.json) · SUCCEEDED
- [impaired-delay-01](impaired-delay-01/trial.json) · SUCCEEDED

## Interpretation

- Experiments describe the isolated local Asterisk lab. Carrier, production and conversational quality conclusions require separate evidence.
- The seeded netem sequence depends on packet order and the host schedule.
- Qdisc drops may include both configured impairment and queue saturation.
- Setup timings are SIP INVITE to first successful response. Echo RTT requires uniquely matched round-trip payloads.
- RTP loss uses sender-to-receiver identity matching. Jitter is the median of final RFC 3550 estimates across streams.
- CPU utilization is process-based, in units of one logical CPU.
- Fewer than five planned repeats per condition; treat observed spread as preliminary.
