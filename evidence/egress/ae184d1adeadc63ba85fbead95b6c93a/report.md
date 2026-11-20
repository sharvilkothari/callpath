# CallPath S5 run

Run `ae184d1adeadc63ba85fbead95b6c93a` · **SUCCEEDED** · cleanup verified

Target 10.200.1.3 over UDP · PCMU, 20 ms · 5 planned repeats

Shaping profile `{"burst_end_pct": 25, "burst_start_pct": 0, "delay_ms": 0, "duplicate_pct": 0, "jitter_ms": 0, "loss_pct": 8.0, "path": "forward", "placement": "egress", "queue_limit": 1000, "reorder_pct": 0, "seed": 42, "traffic": "rtp"}`

## Results by condition

### baseline / loss

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 9.62 | 11.44 | 9.312–14.38 | 2.68 | 5/5 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 208.9 | 208.6 | 206.9–211 | 1.577 | 5/5 | MiB | procfs |
| call_attempts | 8 | 8 | 8–8 | 0 | 5/5 | count | sipp_csv |
| call_setup_latency_max_ms | 6 | 9.4 | 3–25 | 9.182 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 2 | 2.4 | 1–4 | 1.14 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 6 | 9.4 | 3–25 | 9.182 | 5/5 | ms | sipp_rtt |
| concurrent_calls_peak | 4 | 4 | 4–4 | 0 | 5/5 | count | sipp_csv_sampled |
| cps_achieved | 1.438 | 1.437 | 1.435–1.438 | 0.001342 | 5/5 | calls_per_sec | sipp_csv |
| cps_configured | 2 | 2 | 2–2 | 0 | 5/5 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 1 | 1 | 1–1 | 0 | 5/5 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| hangup_causes (16) | 8 | 8 | 8–8 | 0 | 5/5 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 8 | 8 | 8–8 | 0 | 5/5 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| qdisc_drops | 0 | 0 | 0–0 | 0 | 5/5 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | 0 | 5/5 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 0 | 0 | 0–0 | 0 | 5/5 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 0 | 0 | 0–0 | 0 | 5/5 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 6.003 | 6.448 | 1.792–10.36 | 3.358 | 5/5 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 5.985 | 6.384 | 1.567–10.34 | 3.423 | 5/5 | ms | tshark_pcap_rtp |
| rtt_ms | 0.129 | 0.1344 | 0.107–0.1609 | 0.02129 | 5/5 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | 0 | 5/5 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 8 | 8 | 8–8 | 0 | 5/5 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 16 | 16 | 16–16 | 0 | 5/5 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sipp_cpu_pct_peak | 4.859 | 5.741 | 4.83–9.257 | 1.966 | 5/5 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 13.3 | 13.73 | 13.29–15.34 | 0.9008 | 5/5 | MiB | procfs |
| successful_calls | 8 | 8 | 8–8 | 0 | 5/5 | count | sipp_csv |

### impaired / loss

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 14.57 | 14.48 | 9.6–19.48 | 4.79 | 5/5 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 146 | 149.8 | 97.49–208.9 | 48.11 | 5/5 | MiB | procfs |
| call_attempts | 8 | 8 | 8–8 | 0 | 5/5 | count | sipp_csv |
| call_setup_latency_max_ms | 21 | 18.2 | 8–24 | 6.686 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 3 | 2.8 | 2–4 | 0.8367 | 5/5 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 21 | 18.2 | 8–24 | 6.686 | 5/5 | ms | sipp_rtt |
| concurrent_calls_peak | 4 | 4 | 4–4 | 0 | 5/5 | count | sipp_csv_sampled |
| cps_achieved | 1.437 | 1.437 | 1.434–1.438 | 0.001517 | 5/5 | calls_per_sec | sipp_csv |
| cps_configured | 2 | 2 | 2–2 | 0 | 5/5 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 0.9254 | 0.9249 | 0.924–0.9255 | 0.0008349 | 5/5 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| hangup_causes (16) | 8 | 8 | 8–8 | 0 | 5/5 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 8 | 8 | 8–8 | 0 | 5/5 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | 0 | 5/5 | count | asterisk_ami |
| qdisc_drops | 44 | 44.4 | 44–45 | 0.5477 | 5/5 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | 0 | 5/5 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 0 | 0 | 0–0 | 0 | 5/5 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 7.458 | 7.51 | 7.445–7.601 | 0.08349 | 5/5 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 3.175 | 4.252 | 1.305–8.055 | 2.758 | 5/5 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 3.145 | 4.116 | 1.268–8.054 | 2.859 | 5/5 | ms | tshark_pcap_rtp |
| rtt_ms | 0.1571 | 0.1581 | 0.1018–0.2069 | 0.04351 | 5/5 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | 0 | 5/5 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 8 | 8 | 8–8 | 0 | 5/5 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 16 | 16 | 16–16 | 0 | 5/5 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | 0 | 5/5 | count | sipp_csv |
| sipp_cpu_pct_peak | 9.43 | 8.481 | 4.869–9.696 | 2.036 | 5/5 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 13.29 | 12.55 | 11.3–13.41 | 1.092 | 5/5 | MiB | procfs |
| successful_calls | 8 | 8 | 8–8 | 0 | 5/5 | count | sipp_csv |

## Baseline comparison

| Stage / metric | Impaired − baseline median | Unit |
| --- | ---: | --- |
| loss/asterisk_channels_remaining | 0 | count |
| loss/asterisk_cpu_pct_peak | 4.946 | pct_one_logical_cpu |
| loss/asterisk_rss_mib_peak | -62.91 | MiB |
| loss/call_attempts | 0 | count |
| loss/call_setup_latency_max_ms | 15 | ms |
| loss/call_setup_latency_p50_ms | 1 | ms |
| loss/call_setup_latency_p95_ms | 15 | ms |
| loss/concurrent_calls_peak | 0 | count |
| loss/cps_achieved | -0.001 | calls_per_sec |
| loss/cps_configured | 0 | calls_per_sec |
| loss/echo_unique_payload_match_rate | -0.07458 | ratio |
| loss/failed_calls | 0 | count |
| loss/pbx_call_ids_correlated | 0 | count |
| loss/pbx_dtmf_confirmed | 0 | count |
| loss/pbx_transfer_confirmed | 0 | count |
| loss/qdisc_drops | 44 | count |
| loss/qdisc_overlimits | 0 | count |
| loss/rtp_packet_loss_pbx_to_uac | 0 | pct |
| loss/rtp_packet_loss_uac_to_pbx | 7.458 | pct |
| loss/rtp_receiver_jitter_pbx_to_uac | -2.828 | ms |
| loss/rtp_receiver_jitter_uac_to_pbx | -2.841 | ms |
| loss/rtt_ms | 0.02813 | ms |
| loss/scenario_success_rate | 0 | ratio |
| loss/sip_retransmits | 0 | count |
| loss/sip_timeouts | 0 | count |
| loss/sipp_cpu_pct_peak | 4.57 | pct_one_logical_cpu |
| loss/sipp_rss_mib_peak | -0.01562 | MiB |
| loss/successful_calls | 0 | count |

## Acceptance

| Check | Observed | Threshold | Result |
| --- | ---: | ---: | --- |
| baseline/loss minimum scenario success | 1 | `>= 0.99` | PASS |
| impaired/loss minimum scenario success | 1 | `>= 0.8` | PASS |
| impaired/loss uac_to_pbx median loss delta (pp) | 7.458 | `<= 13.0` | PASS |

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
