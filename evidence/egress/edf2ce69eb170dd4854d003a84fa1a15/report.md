# CallPath S7 run

Run `edf2ce69eb170dd4854d003a84fa1a15` · **SUCCEEDED** · cleanup verified

Target 10.200.1.3 over UDP · PCMU, 20 ms · 5 planned repeats

Shaping profile `{"burst_end_pct": 25, "burst_start_pct": 0, "delay_ms": 40, "duplicate_pct": 0, "jitter_ms": 10, "loss_pct": 0, "path": "both", "placement": "egress", "queue_limit": 1000, "reorder_pct": 0, "seed": 42, "traffic": "rtp"}`

## Results by condition

### baseline / echo

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 18.29 | 20.39 | 14.51–32.15 | 6.799 | 5/5 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 209.6 | 209.8 | 208.8–211 | 0.9355 | 5/5 | MiB | procfs |
| call_attempts | 5 | 5 | 5–5 | 0 | 5/5 | count | sipp_csv |
| call_setup_latency_max_ms | 6 | 9.8 | 4–27 | 9.68 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 3 | 4 | 3–7 | 1.732 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 6 | 9.8 | 4–27 | 9.68 | 5/5 | ms | sipp_rtt |
| concurrent_calls_peak | 4 | 4 | 4–4 | 0 | 5/5 | count | sipp_csv_sampled |
| cps_achieved | 1.094 | 1.093 | 1.09–1.095 | 0.001949 | 5/5 | calls_per_sec | sipp_csv |
| cps_configured | 2 | 2 | 2–2 | 0 | 5/5 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 1 | 1 | 1–1 | 0 | 5/5 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| hangup_causes (16) | 5 | 5 | 5–5 | 0 | 5/5 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 5 | 5 | 5–5 | 0 | 5/5 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| qdisc_drops | 0 | 0 | 0–0 | 0 | 5/5 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | 0 | 5/5 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 0 | 0 | 0–0 | 0 | 4/5 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 0 | 0 | 0–0 | 0 | 5/5 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 6.84 | 6.528 | 4.415–8.018 | 1.655 | 4/5 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 6.771 | 7.285 | 4.894–10.71 | 2.223 | 5/5 | ms | tshark_pcap_rtp |
| rtt_ms | 0.2191 | 0.2204 | 0.21–0.232 | 0.008395 | 5/5 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | 0 | 5/5 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 5 | 5 | 5–5 | 0 | 5/5 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 10 | 10 | 10–10 | 0 | 5/5 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sipp_cpu_pct_peak | 9.232 | 8.366 | 4.764–9.597 | 2.031 | 5/5 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 15.21 | 14.6 | 13.55–15.38 | 0.9551 | 5/5 | MiB | procfs |
| successful_calls | 5 | 5 | 5–5 | 0 | 5/5 | count | sipp_csv |

### impaired / echo

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 9.632 | 11.36 | 9.437–18.6 | 4.045 | 5/5 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 210.7 | 210.5 | 208.8–212.8 | 1.703 | 5/5 | MiB | procfs |
| call_attempts | 5 | 5 | 5–5 | 0 | 5/5 | count | sipp_csv |
| call_setup_latency_max_ms | 4 | 9.2 | 4–29 | 11.08 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 4 | 3.6 | 3–4 | 0.5477 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 4 | 9.2 | 4–29 | 11.08 | 5/5 | ms | sipp_rtt |
| concurrent_calls_peak | 4 | 4 | 4–4 | 0 | 5/5 | count | sipp_csv_sampled |
| cps_achieved | 1.095 | 1.095 | 1.094–1.096 | 0.0008367 | 5/5 | calls_per_sec | sipp_csv |
| cps_configured | 2 | 2 | 2–2 | 0 | 5/5 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 0.9798 | 0.9797 | 0.9756–0.9837 | 0.003206 | 5/5 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| hangup_causes (16) | 5 | 5 | 5–5 | 0 | 5/5 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 5 | 5 | 5–5 | 0 | 5/5 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| qdisc_drops | 0 | 0 | 0–0 | 0 | 5/5 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | 0 | 5/5 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 0 | 0 | 0–0 | 0 | 5/5 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 0 | 0 | 0–0 | 0 | 5/5 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 19.32 | 19.18 | 16.94–23.06 | 2.456 | 5/5 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 12.34 | 13.02 | 12.04–15.11 | 1.307 | 5/5 | ms | tshark_pcap_rtp |
| rtt_ms | 81.62 | 81.56 | 81.16–81.91 | 0.2758 | 5/5 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | 0 | 5/5 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 5 | 5 | 5–5 | 0 | 5/5 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 10 | 10 | 10–10 | 0 | 5/5 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sipp_cpu_pct_peak | 4.836 | 5.756 | 4.8–9.456 | 2.068 | 5/5 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 13.55 | 14.15 | 13.43–15.36 | 0.912 | 5/5 | MiB | procfs |
| successful_calls | 5 | 5 | 5–5 | 0 | 5/5 | count | sipp_csv |

## Baseline comparison

| Stage / metric | Impaired − baseline median | Unit |
| --- | ---: | --- |
| echo/asterisk_channels_remaining | 0 | count |
| echo/asterisk_cpu_pct_peak | -8.657 | pct_one_logical_cpu |
| echo/asterisk_rss_mib_peak | 1.184 | MiB |
| echo/call_attempts | 0 | count |
| echo/call_setup_latency_max_ms | -2 | ms |
| echo/call_setup_latency_p50_ms | 1 | ms |
| echo/call_setup_latency_p95_ms | -2 | ms |
| echo/concurrent_calls_peak | 0 | count |
| echo/cps_achieved | 0.001 | calls_per_sec |
| echo/cps_configured | 0 | calls_per_sec |
| echo/echo_unique_payload_match_rate | -0.02024 | ratio |
| echo/failed_calls | 0 | count |
| echo/pbx_call_ids_correlated | 0 | count |
| echo/pbx_dtmf_confirmed | 0 | count |
| echo/pbx_transfer_confirmed | 0 | count |
| echo/qdisc_drops | 0 | count |
| echo/qdisc_overlimits | 0 | count |
| echo/rtp_packet_loss_pbx_to_uac | 0 | pct |
| echo/rtp_packet_loss_uac_to_pbx | 0 | pct |
| echo/rtp_receiver_jitter_pbx_to_uac | 12.48 | ms |
| echo/rtp_receiver_jitter_uac_to_pbx | 5.572 | ms |
| echo/rtt_ms | 81.4 | ms |
| echo/scenario_success_rate | 0 | ratio |
| echo/sip_retransmits | 0 | count |
| echo/sip_timeouts | 0 | count |
| echo/sipp_cpu_pct_peak | -4.396 | pct_one_logical_cpu |
| echo/sipp_rss_mib_peak | -1.656 | MiB |
| echo/successful_calls | 0 | count |

## Acceptance

| Check | Observed | Threshold | Result |
| --- | ---: | ---: | --- |
| baseline/echo minimum scenario success | 1 | `>= 0.99` | PASS |
| baseline/echo minimum unique payload echo coverage | 1 | `>= 0.8` | PASS |
| impaired/echo minimum scenario success | 1 | `>= 0.95` | PASS |
| impaired/echo minimum unique payload echo coverage | 0.9756 | `>= 0.6` | PASS |

## Evidence

- [Run snapshot](snapshot.json)
- [Machine-readable report](report.json)
- [Artifact manifest](artifacts.json)
- [baseline-echo-01](baseline-echo-01/trial.json) · SUCCEEDED
- [baseline-echo-02](baseline-echo-02/trial.json) · SUCCEEDED
- [baseline-echo-03](baseline-echo-03/trial.json) · SUCCEEDED
- [baseline-echo-04](baseline-echo-04/trial.json) · SUCCEEDED
- [baseline-echo-05](baseline-echo-05/trial.json) · SUCCEEDED
- [impaired-echo-01](impaired-echo-01/trial.json) · SUCCEEDED
- [impaired-echo-02](impaired-echo-02/trial.json) · SUCCEEDED
- [impaired-echo-03](impaired-echo-03/trial.json) · SUCCEEDED
- [impaired-echo-04](impaired-echo-04/trial.json) · SUCCEEDED
- [impaired-echo-05](impaired-echo-05/trial.json) · SUCCEEDED

## Interpretation

- Experiments describe the isolated local Asterisk lab. Carrier, production and conversational quality conclusions require separate evidence.
- The seeded netem sequence depends on packet order and the host schedule.
- Qdisc drops may include both configured impairment and queue saturation.
- Setup timings are SIP INVITE to first successful response. Echo RTT requires uniquely matched round-trip payloads.
- RTP loss uses sender-to-receiver identity matching. Jitter is the median of final RFC 3550 estimates across streams.
- CPU utilization is process-based, in units of one logical CPU.
