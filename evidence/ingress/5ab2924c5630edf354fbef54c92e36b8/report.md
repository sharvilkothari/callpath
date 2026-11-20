# CallPath S5 run

Run `5ab2924c5630edf354fbef54c92e36b8` · **SUCCEEDED** · cleanup verified

Target 10.200.1.3 over UDP · PCMU, 20 ms · 5 planned repeats

Shaping profile `{"burst_end_pct": 25, "burst_start_pct": 0, "delay_ms": 0, "duplicate_pct": 0, "jitter_ms": 0, "loss_pct": 8.0, "path": "both", "placement": "ingress", "queue_limit": 1000, "reorder_pct": 0, "seed": 42, "traffic": "rtp"}`

## Results by condition

### baseline / loss

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 4.969 | 4.929 | 4.829–4.974 | 0.06375 | 5/5 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 148.9 | 148.5 | 147–149.1 | 0.8957 | 5/5 | MiB | procfs |
| call_attempts | 6 | 6 | 6–6 | 0 | 5/5 | count | sipp_csv |
| call_setup_latency_max_ms | 3 | 3.2 | 2–5 | 1.304 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 2 | 1.6 | 1–2 | 0.5477 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 3 | 3.2 | 2–5 | 1.304 | 5/5 | ms | sipp_rtt |
| concurrent_calls_peak | 4 | 4 | 4–4 | 0 | 5/5 | count | sipp_csv_sampled |
| cps_achieved | 1.315 | 1.315 | 1.315–1.316 | 0.0005477 | 5/5 | calls_per_sec | sipp_csv |
| cps_configured | 2 | 2 | 2–2 | 0 | 5/5 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 1 | 1 | 1–1 | 0 | 5/5 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| hangup_causes (16) | 6 | 6 | 6–6 | 0 | 5/5 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 6 | 6 | 6–6 | 0 | 5/5 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| qdisc_drops | 0 | 0 | 0–0 | 0 | 5/5 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | 0 | 5/5 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 0 | 0 | 0–0 | 0 | 5/5 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 0 | 0 | 0–0 | 0 | 5/5 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 6.392 | 6.566 | 5.274–7.607 | 1.008 | 5/5 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 6.585 | 6.737 | 5.28–7.815 | 1.022 | 5/5 | ms | tshark_pcap_rtp |
| rtt_ms | 0.08512 | 0.08526 | 0.0782–0.09394 | 0.006126 | 5/5 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | 0 | 5/5 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 6 | 6 | 6–6 | 0 | 5/5 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 12 | 12 | 12–12 | 0 | 5/5 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sipp_cpu_pct_peak | 4.968 | 5.927 | 4.87–9.942 | 2.245 | 5/5 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 15.24 | 14.59 | 13.5–15.4 | 0.9972 | 5/5 | MiB | procfs |
| successful_calls | 6 | 6 | 6–6 | 0 | 5/5 | count | sipp_csv |

### impaired / loss

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 9.409 | 8.579 | 4.837–9.917 | 2.125 | 5/5 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 146.6 | 147 | 146.6–148.8 | 0.9946 | 5/5 | MiB | procfs |
| call_attempts | 6 | 6 | 6–6 | 0 | 5/5 | count | sipp_csv |
| call_setup_latency_max_ms | 4 | 3.6 | 3–4 | 0.5477 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 2 | 2.2 | 2–3 | 0.4472 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 4 | 3.6 | 3–4 | 0.5477 | 5/5 | ms | sipp_rtt |
| concurrent_calls_peak | 4 | 4 | 4–4 | 0 | 5/5 | count | sipp_csv_sampled |
| cps_achieved | 1.315 | 1.315 | 1.314–1.315 | 0.0004472 | 5/5 | calls_per_sec | sipp_csv |
| cps_configured | 2 | 2 | 2–2 | 0 | 5/5 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 0.8575 | 0.8575 | 0.8571–0.8578 | 0.000228 | 5/5 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| hangup_causes (16) | 6 | 6 | 6–6 | 0 | 5/5 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 6 | 6 | 6–6 | 0 | 5/5 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| qdisc_drops | 63 | 63 | 63–63 | 0 | 5/5 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | 0 | 5/5 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 7.561 | 7.561 | 7.543–7.579 | 0.01304 | 5/5 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 7.24 | 7.24 | 7.223–7.256 | 0.01158 | 5/5 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 7.061 | 6.955 | 6.074–8.368 | 0.9269 | 5/5 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 6.767 | 6.922 | 5.762–8.168 | 0.8917 | 5/5 | ms | tshark_pcap_rtp |
| rtt_ms | 0.1049 | 0.1076 | 0.09203–0.1271 | 0.01273 | 5/5 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | 0 | 5/5 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 6 | 6 | 6–6 | 0 | 5/5 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 12 | 12 | 12–12 | 0 | 5/5 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sipp_cpu_pct_peak | 4.967 | 7.451 | 4.885–12.77 | 3.612 | 5/5 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 15.31 | 14.69 | 13.5–15.64 | 1.089 | 5/5 | MiB | procfs |
| successful_calls | 6 | 6 | 6–6 | 0 | 5/5 | count | sipp_csv |

## Baseline comparison

| Stage / metric | Impaired − baseline median | Unit |
| --- | ---: | --- |
| loss/asterisk_channels_remaining | 0 | count |
| loss/asterisk_cpu_pct_peak | 4.44 | pct_one_logical_cpu |
| loss/asterisk_rss_mib_peak | -2.324 | MiB |
| loss/call_attempts | 0 | count |
| loss/call_setup_latency_max_ms | 1 | ms |
| loss/call_setup_latency_p50_ms | 0 | ms |
| loss/call_setup_latency_p95_ms | 1 | ms |
| loss/concurrent_calls_peak | 0 | count |
| loss/cps_achieved | 0 | calls_per_sec |
| loss/cps_configured | 0 | calls_per_sec |
| loss/echo_unique_payload_match_rate | -0.1425 | ratio |
| loss/failed_calls | 0 | count |
| loss/pbx_call_ids_correlated | 0 | count |
| loss/pbx_dtmf_confirmed | 0 | count |
| loss/pbx_transfer_confirmed | 0 | count |
| loss/qdisc_drops | 63 | count |
| loss/qdisc_overlimits | 0 | count |
| loss/rtp_packet_loss_pbx_to_uac | 7.561 | pct |
| loss/rtp_packet_loss_uac_to_pbx | 7.24 | pct |
| loss/rtp_receiver_jitter_pbx_to_uac | 0.669 | ms |
| loss/rtp_receiver_jitter_uac_to_pbx | 0.1822 | ms |
| loss/rtt_ms | 0.01979 | ms |
| loss/scenario_success_rate | 0 | ratio |
| loss/sip_retransmits | 0 | count |
| loss/sip_timeouts | 0 | count |
| loss/sipp_cpu_pct_peak | -0.001855 | pct_one_logical_cpu |
| loss/sipp_rss_mib_peak | 0.07422 | MiB |
| loss/successful_calls | 0 | count |

## Acceptance

| Check | Observed | Threshold | Result |
| --- | ---: | ---: | --- |
| baseline/loss minimum scenario success | 1 | `>= 0.99` | PASS |
| impaired/loss minimum scenario success | 1 | `>= 0.8` | PASS |
| impaired/loss uac_to_pbx median loss delta (pp) | 7.24 | `<= 13.0` | PASS |
| impaired/loss pbx_to_uac median loss delta (pp) | 7.561 | `<= 13.0` | PASS |

## Evidence

- [Run snapshot](snapshot.json)
- [Machine-readable report](report.json)
- [Artifact manifest](artifacts.json)
- [baseline-loss-01](baseline-loss-01/trial.json) · SUCCEEDED
- [baseline-loss-02](baseline-loss-02/trial.json) · SUCCEEDED
- [baseline-loss-03](baseline-loss-03/trial.json) · SUCCEEDED
- [baseline-loss-04](baseline-loss-04/trial.json) · SUCCEEDED
- [baseline-loss-05](baseline-loss-05/trial.json) · SUCCEEDED
- [impaired-loss-01](impaired-loss-01/trial.json) · SUCCEEDED
- [impaired-loss-02](impaired-loss-02/trial.json) · SUCCEEDED
- [impaired-loss-03](impaired-loss-03/trial.json) · SUCCEEDED
- [impaired-loss-04](impaired-loss-04/trial.json) · SUCCEEDED
- [impaired-loss-05](impaired-loss-05/trial.json) · SUCCEEDED

## Interpretation

- Experiments describe the isolated local Asterisk lab. Carrier, production and conversational quality conclusions require separate evidence.
- The seeded netem sequence depends on packet order and the host schedule.
- Qdisc drops may include both configured impairment and queue saturation.
- Setup timings are SIP INVITE to first successful response. Echo RTT requires uniquely matched round-trip payloads.
- RTP loss uses sender-to-receiver identity matching. Jitter is the median of final RFC 3550 estimates across streams.
- CPU utilization is process-based, in units of one logical CPU.
