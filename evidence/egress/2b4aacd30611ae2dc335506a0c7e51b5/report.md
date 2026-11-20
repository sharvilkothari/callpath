# CallPath S2 run

Run `2b4aacd30611ae2dc335506a0c7e51b5` · **SUCCEEDED** · cleanup verified

Target 10.200.1.3 over UDP · PCMU, 20 ms · 1 planned repeats

Shaping profile `{"burst_end_pct": 25, "burst_start_pct": 0, "delay_ms": 0, "duplicate_pct": 0, "jitter_ms": 0, "loss_pct": 0, "path": "forward", "placement": "egress", "queue_limit": 1000, "reorder_pct": 0, "seed": 42, "traffic": "all"}`

## Results by condition

### baseline / ramp-2

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 18.95 | 18.95 | 18.95–18.95 | — | 1/1 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 210.8 | 210.8 | 210.8–210.8 | — | 1/1 | MiB | procfs |
| call_attempts | 12 | 12 | 12–12 | — | 1/1 | count | sipp_csv |
| call_setup_latency_max_ms | 6 | 6 | 6–6 | — | 1/1 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 3 | 3 | 3–3 | — | 1/1 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 6 | 6 | 6–6 | — | 1/1 | ms | sipp_rtt |
| concurrent_calls_peak | 5 | 5 | 5–5 | — | 1/1 | count | sipp_csv_sampled |
| cps_achieved | 1.487 | 1.487 | 1.487–1.487 | — | 1/1 | calls_per_sec | sipp_csv |
| cps_configured | 2 | 2 | 2–2 | — | 1/1 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 1 | 1 | 1–1 | — | 1/1 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| hangup_causes (16) | 12 | 12 | 12–12 | — | 1/1 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 12 | 12 | 12–12 | — | 1/1 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_ami |
| qdisc_drops | 0 | 0 | 0–0 | — | 1/1 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | — | 1/1 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 0 | 0 | 0–0 | — | 1/1 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 0 | 0 | 0–0 | — | 1/1 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 7.896 | 7.896 | 7.896–7.896 | — | 1/1 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 7.799 | 7.799 | 7.799–7.799 | — | 1/1 | ms | tshark_pcap_rtp |
| rtt_ms | 0.1969 | 0.1969 | 0.1969–0.1969 | — | 1/1 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | — | 1/1 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 12 | 12 | 12–12 | — | 1/1 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 24 | 24 | 24–24 | — | 1/1 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| sipp_cpu_pct_peak | 9.012 | 9.012 | 9.012–9.012 | — | 1/1 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 13.37 | 13.37 | 13.37–13.37 | — | 1/1 | MiB | procfs |
| successful_calls | 12 | 12 | 12–12 | — | 1/1 | count | sipp_csv |

### baseline / ramp-5

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 66.13 | 66.13 | 66.13–66.13 | — | 1/1 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 219 | 219 | 219–219 | — | 1/1 | MiB | procfs |
| call_attempts | 30 | 30 | 30–30 | — | 1/1 | count | sipp_csv |
| call_setup_latency_max_ms | 3 | 3 | 3–3 | — | 1/1 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 2 | 2 | 2–2 | — | 1/1 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 3 | 3 | 3–3 | — | 1/1 | ms | sipp_rtt |
| concurrent_calls_peak | 11 | 11 | 11–11 | — | 1/1 | count | sipp_csv_sampled |
| cps_achieved | 3.716 | 3.716 | 3.716–3.716 | — | 1/1 | calls_per_sec | sipp_csv |
| cps_configured | 5 | 5 | 5–5 | — | 1/1 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 1 | 1 | 1–1 | — | 1/1 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| hangup_causes (16) | 30 | 30 | 30–30 | — | 1/1 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 30 | 30 | 30–30 | — | 1/1 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_ami |
| qdisc_drops | 0 | 0 | 0–0 | — | 1/1 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | — | 1/1 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 0 | 0 | 0–0 | — | 1/1 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 0 | 0 | 0–0 | — | 1/1 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 8.551 | 8.551 | 8.551–8.551 | — | 1/1 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 8.075 | 8.075 | 8.075–8.075 | — | 1/1 | ms | tshark_pcap_rtp |
| rtt_ms | 0.185 | 0.185 | 0.185–0.185 | — | 1/1 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | — | 1/1 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 30 | 30 | 30–30 | — | 1/1 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 60 | 60 | 60–60 | — | 1/1 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| sipp_cpu_pct_peak | 9.543 | 9.543 | 9.543–9.543 | — | 1/1 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 15.47 | 15.47 | 15.47–15.47 | — | 1/1 | MiB | procfs |
| successful_calls | 30 | 30 | 30–30 | — | 1/1 | count | sipp_csv |

### baseline / ramp-10

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 36.37 | 36.37 | 36.37–36.37 | — | 1/1 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 223.2 | 223.2 | 223.2–223.2 | — | 1/1 | MiB | procfs |
| call_attempts | 60 | 60 | 60–60 | — | 1/1 | count | sipp_csv |
| call_setup_latency_max_ms | 6 | 6 | 6–6 | — | 1/1 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 3 | 3 | 3–3 | — | 1/1 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 4 | 4 | 4–4 | — | 1/1 | ms | sipp_rtt |
| concurrent_calls_peak | 21 | 21 | 21–21 | — | 1/1 | count | sipp_csv_sampled |
| cps_achieved | 7.434 | 7.434 | 7.434–7.434 | — | 1/1 | calls_per_sec | sipp_csv |
| cps_configured | 10 | 10 | 10–10 | — | 1/1 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 0.9998 | 0.9998 | 0.9998–0.9998 | — | 1/1 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| hangup_causes (16) | 60 | 60 | 60–60 | — | 1/1 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 60 | 60 | 60–60 | — | 1/1 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | — | 1/1 | count | asterisk_ami |
| qdisc_drops | 0 | 0 | 0–0 | — | 1/1 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | — | 1/1 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 0 | 0 | 0–0 | — | 1/1 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 0 | 0 | 0–0 | — | 1/1 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 7.03 | 7.03 | 7.03–7.03 | — | 1/1 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 6.945 | 6.945 | 6.945–6.945 | — | 1/1 | ms | tshark_pcap_rtp |
| rtt_ms | 0.1512 | 0.1512 | 0.1512–0.1512 | — | 1/1 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | — | 1/1 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 60 | 60 | 60–60 | — | 1/1 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 120 | 120 | 120–120 | — | 1/1 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | — | 1/1 | count | sipp_csv |
| sipp_cpu_pct_peak | 14.25 | 14.25 | 14.25–14.25 | — | 1/1 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 17.68 | 17.68 | 17.68–17.68 | — | 1/1 | MiB | procfs |
| successful_calls | 60 | 60 | 60–60 | — | 1/1 | count | sipp_csv |

## Baseline comparison

| Stage / metric | Impaired − baseline median | Unit |
| --- | ---: | --- |

## Acceptance

| Check | Observed | Threshold | Result |
| --- | ---: | ---: | --- |
| baseline/ramp-2 minimum scenario success | 1 | `>= 0.99` | PASS |
| baseline/ramp-5 minimum scenario success | 1 | `>= 0.99` | PASS |
| baseline/ramp-10 minimum scenario success | 1 | `>= 0.99` | PASS |

## Evidence

- [Run snapshot](snapshot.json)
- [Machine-readable report](report.json)
- [Artifact manifest](artifacts.json)
- [baseline-ramp-2-01](baseline-ramp-2-01/trial.json) · SUCCEEDED
- [baseline-ramp-5-01](baseline-ramp-5-01/trial.json) · SUCCEEDED
- [baseline-ramp-10-01](baseline-ramp-10-01/trial.json) · SUCCEEDED

## Interpretation

- Experiments describe the isolated local Asterisk lab. Carrier, production and conversational quality conclusions require separate evidence.
- The seeded netem sequence depends on packet order and the host schedule.
- Qdisc drops may include both configured impairment and queue saturation.
- Setup timings are SIP INVITE to first successful response. Echo RTT requires uniquely matched round-trip payloads.
- RTP loss uses sender-to-receiver identity matching. Jitter is the median of final RFC 3550 estimates across streams.
- CPU utilization is process-based, in units of one logical CPU.
- Fewer than five planned repeats per condition; treat observed spread as preliminary.
