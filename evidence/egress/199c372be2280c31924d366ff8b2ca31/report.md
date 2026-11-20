# CallPath S4 run

Run `199c372be2280c31924d366ff8b2ca31` · **SUCCEEDED** · cleanup verified

Target 10.200.1.3 over UDP · PCMU, 20 ms · 5 planned repeats

Shaping profile `{"burst_end_pct": 25, "burst_start_pct": 0, "delay_ms": 80, "duplicate_pct": 0, "jitter_ms": 20, "loss_pct": 0, "path": "forward", "placement": "egress", "queue_limit": 1000, "reorder_pct": 0, "seed": 42, "traffic": "sip"}`

## Results by condition

### baseline / delay

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 9.481 | 10.27 | 9.141–14.03 | 2.109 | 5/5 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 209.2 | 209.4 | 208.8–210.8 | 0.8244 | 5/5 | MiB | procfs |
| call_attempts | 5 | 5 | 5–5 | 0 | 5/5 | count | sipp_csv |
| call_setup_latency_max_ms | 7 | 9.4 | 5–19 | 5.55 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 4 | 4.2 | 4–5 | 0.4472 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 7 | 9.4 | 5–19 | 5.55 | 5/5 | ms | sipp_rtt |
| concurrent_calls_peak | 4 | 4 | 4–4 | 0 | 5/5 | count | sipp_csv_sampled |
| cps_achieved | 1.227 | 1.228 | 1.226–1.229 | 0.001342 | 5/5 | calls_per_sec | sipp_csv |
| cps_configured | 2 | 2 | 2–2 | 0 | 5/5 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 1 | 0.9995 | 0.9973–1 | 0.001209 | 5/5 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| hangup_causes (16) | 5 | 5 | 5–5 | 0 | 5/5 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 5 | 5 | 5–5 | 0 | 5/5 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| qdisc_drops | 0 | 0 | 0–0 | 0 | 5/5 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | 0 | 5/5 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 0 | 0 | 0–0 | 0 | 5/5 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 0 | 0 | 0–0 | 0 | 5/5 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 8.027 | 8.64 | 7.035–11.31 | 1.668 | 5/5 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 7.967 | 8.589 | 7.063–11.28 | 1.687 | 5/5 | ms | tshark_pcap_rtp |
| rtt_ms | 0.2332 | 0.2346 | 0.2091–0.262 | 0.02171 | 5/5 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | 0 | 5/5 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 5 | 5 | 5–5 | 0 | 5/5 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 10 | 10 | 10–10 | 0 | 5/5 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sipp_cpu_pct_peak | 9.166 | 8.386 | 4.764–9.512 | 2.031 | 5/5 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 13.55 | 14.22 | 13.3–17.03 | 1.58 | 5/5 | MiB | procfs |
| successful_calls | 5 | 5 | 5–5 | 0 | 5/5 | count | sipp_csv |

### impaired / delay

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 14.16 | 12.96 | 4.859–18.71 | 5.828 | 5/5 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 209 | 208.7 | 206.9–209.4 | 1.059 | 5/5 | MiB | procfs |
| call_attempts | 5 | 5 | 5–5 | 0 | 5/5 | count | sipp_csv |
| call_setup_latency_max_ms | 98 | 99.4 | 95–104 | 3.912 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 74 | 74.8 | 73–79 | 2.49 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 98 | 99.4 | 95–104 | 3.912 | 5/5 | ms | sipp_rtt |
| concurrent_calls_peak | 4 | 4 | 4–4 | 0 | 5/5 | count | sipp_csv_sampled |
| cps_achieved | 1.196 | 1.196 | 1.195–1.198 | 0.001304 | 5/5 | calls_per_sec | sipp_csv |
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
| rtp_receiver_jitter_pbx_to_uac | 5.924 | 6.041 | 3.63–8.372 | 1.762 | 5/5 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 5.903 | 6.073 | 3.614–8.821 | 1.904 | 5/5 | ms | tshark_pcap_rtp |
| rtt_ms | 0.227 | 0.2182 | 0.1411–0.258 | 0.04499 | 5/5 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | 0 | 5/5 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 5 | 5 | 5–5 | 0 | 5/5 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 10 | 10 | 10–10 | 0 | 5/5 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sipp_cpu_pct_peak | 9.181 | 7.487 | 4.751–9.439 | 2.451 | 5/5 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 13.5 | 13.76 | 13.3–15.02 | 0.7128 | 5/5 | MiB | procfs |
| successful_calls | 5 | 5 | 5–5 | 0 | 5/5 | count | sipp_csv |

## Baseline comparison

| Stage / metric | Impaired − baseline median | Unit |
| --- | ---: | --- |
| delay/asterisk_channels_remaining | 0 | count |
| delay/asterisk_cpu_pct_peak | 4.678 | pct_one_logical_cpu |
| delay/asterisk_rss_mib_peak | -0.1211 | MiB |
| delay/call_attempts | 0 | count |
| delay/call_setup_latency_max_ms | 91 | ms |
| delay/call_setup_latency_p50_ms | 70 | ms |
| delay/call_setup_latency_p95_ms | 91 | ms |
| delay/concurrent_calls_peak | 0 | count |
| delay/cps_achieved | -0.031 | calls_per_sec |
| delay/cps_configured | 0 | calls_per_sec |
| delay/echo_unique_payload_match_rate | 0 | ratio |
| delay/failed_calls | 0 | count |
| delay/pbx_call_ids_correlated | 0 | count |
| delay/pbx_dtmf_confirmed | 0 | count |
| delay/pbx_transfer_confirmed | 0 | count |
| delay/qdisc_drops | 0 | count |
| delay/qdisc_overlimits | 0 | count |
| delay/rtp_packet_loss_pbx_to_uac | 0 | pct |
| delay/rtp_packet_loss_uac_to_pbx | 0 | pct |
| delay/rtp_receiver_jitter_pbx_to_uac | -2.103 | ms |
| delay/rtp_receiver_jitter_uac_to_pbx | -2.064 | ms |
| delay/rtt_ms | -0.006199 | ms |
| delay/scenario_success_rate | 0 | ratio |
| delay/sip_retransmits | 0 | count |
| delay/sip_timeouts | 0 | count |
| delay/sipp_cpu_pct_peak | 0.01445 | pct_one_logical_cpu |
| delay/sipp_rss_mib_peak | -0.05859 | MiB |
| delay/successful_calls | 0 | count |

## Acceptance

| Check | Observed | Threshold | Result |
| --- | ---: | ---: | --- |
| baseline/delay minimum scenario success | 1 | `>= 0.99` | PASS |
| impaired/delay minimum scenario success | 1 | `>= 0.95` | PASS |
| impaired/delay median setup p95 delta (ms) | 91 | `<= 240` | PASS |

## Evidence

- [Run snapshot](snapshot.json)
- [Machine-readable report](report.json)
- [Artifact manifest](artifacts.json)
- [baseline-delay-01](baseline-delay-01/trial.json) · SUCCEEDED
- [baseline-delay-02](baseline-delay-02/trial.json) · SUCCEEDED
- [baseline-delay-03](baseline-delay-03/trial.json) · SUCCEEDED
- [baseline-delay-04](baseline-delay-04/trial.json) · SUCCEEDED
- [baseline-delay-05](baseline-delay-05/trial.json) · SUCCEEDED
- [impaired-delay-01](impaired-delay-01/trial.json) · SUCCEEDED
- [impaired-delay-02](impaired-delay-02/trial.json) · SUCCEEDED
- [impaired-delay-03](impaired-delay-03/trial.json) · SUCCEEDED
- [impaired-delay-04](impaired-delay-04/trial.json) · SUCCEEDED
- [impaired-delay-05](impaired-delay-05/trial.json) · SUCCEEDED

## Interpretation

- Experiments describe the isolated local Asterisk lab. Carrier, production and conversational quality conclusions require separate evidence.
- The seeded netem sequence depends on packet order and the host schedule.
- Qdisc drops may include both configured impairment and queue saturation.
- Setup timings are SIP INVITE to first successful response. Echo RTT requires uniquely matched round-trip payloads.
- RTP loss uses sender-to-receiver identity matching. Jitter is the median of final RFC 3550 estimates across streams.
- CPU utilization is process-based, in units of one logical CPU.
