# CallPath S5 run

Run `569b36d08c7ff06eed2242c2d878bcfb` · **SUCCEEDED** · cleanup verified

Target 10.200.1.3 over UDP · PCMU, 20 ms · 2 planned repeats

Shaping profile `{"burst_end_pct": 40.0, "burst_start_pct": 5.0, "delay_ms": 0, "duplicate_pct": 0, "jitter_ms": 0, "loss_pct": 0, "path": "reverse", "placement": "egress", "queue_limit": 1000, "reorder_pct": 0, "seed": 42, "traffic": "rtp"}`

## Results by condition

### baseline / loss

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | 0 | 2/2 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 12.09 | 12.09 | 9.734–14.44 | 3.327 | 2/2 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 208.1 | 208.1 | 207.2–209 | 1.237 | 2/2 | MiB | procfs |
| call_attempts | 5 | 5 | 5–5 | 0 | 2/2 | count | sipp_csv |
| call_setup_latency_max_ms | 10.5 | 10.5 | 5–16 | 7.778 | 2/2 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 2.5 | 2.5 | 2–3 | 0.7071 | 2/2 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 10.5 | 10.5 | 5–16 | 7.778 | 2/2 | ms | sipp_rtt |
| concurrent_calls_peak | 4 | 4 | 4–4 | 0 | 2/2 | count | sipp_csv_sampled |
| cps_achieved | 1.23 | 1.23 | 1.229–1.23 | 0.0007071 | 2/2 | calls_per_sec | sipp_csv |
| cps_configured | 2 | 2 | 2–2 | 0 | 2/2 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 1 | 1 | 1–1 | 0 | 2/2 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | 0 | 2/2 | count | sipp_csv |
| hangup_causes (16) | 5 | 5 | 5–5 | 0 | 2/2 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 5 | 5 | 5–5 | 0 | 2/2 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | 0 | 2/2 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | 0 | 2/2 | count | asterisk_ami |
| qdisc_drops | 0 | 0 | 0–0 | 0 | 2/2 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | 0 | 2/2 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 0 | 0 | 0–0 | 0 | 2/2 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 0 | 0 | 0–0 | 0 | 2/2 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 4.404 | 4.404 | 3.514–5.294 | 1.259 | 2/2 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 4.355 | 4.355 | 3.437–5.274 | 1.299 | 2/2 | ms | tshark_pcap_rtp |
| rtt_ms | 0.1335 | 0.1335 | 0.123–0.144 | 0.01484 | 2/2 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | 0 | 2/2 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 5 | 5 | 5–5 | 0 | 2/2 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 10 | 10 | 10–10 | 0 | 2/2 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | 0 | 2/2 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | 0 | 2/2 | count | sipp_csv |
| sipp_cpu_pct_peak | 4.875 | 4.875 | 4.851–4.899 | 0.03361 | 2/2 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 13.3 | 13.3 | 13.29–13.3 | 0.01105 | 2/2 | MiB | procfs |
| successful_calls | 5 | 5 | 5–5 | 0 | 2/2 | count | sipp_csv |

### impaired / loss

| Metric | Median | Mean | Min–max | SD | Samples | Unit | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| asterisk_channels_remaining | 0 | 0 | 0–0 | 0 | 2/2 | count | asterisk_cli |
| asterisk_cpu_pct_peak | 9.556 | 9.556 | 9.4–9.711 | 0.2199 | 2/2 | pct_one_logical_cpu | procfs |
| asterisk_rss_mib_peak | 209 | 209 | 206.9–211.1 | 3.011 | 2/2 | MiB | procfs |
| call_attempts | 5 | 5 | 5–5 | 0 | 2/2 | count | sipp_csv |
| call_setup_latency_max_ms | 20 | 20 | 7–33 | 18.38 | 2/2 | ms | sipp_rtt |
| call_setup_latency_p50_ms | 4 | 4 | 2–6 | 2.828 | 2/2 | ms | sipp_rtt |
| call_setup_latency_p95_ms | 20 | 20 | 7–33 | 18.38 | 2/2 | ms | sipp_rtt |
| concurrent_calls_peak | 4 | 4 | 4–4 | 0 | 2/2 | count | sipp_csv_sampled |
| cps_achieved | 1.229 | 1.229 | 1.229–1.229 | 0 | 2/2 | calls_per_sec | sipp_csv |
| cps_configured | 2 | 2 | 2–2 | 0 | 2/2 | calls_per_sec | run_snapshot |
| echo_unique_payload_match_rate | 0.9404 | 0.9404 | 0.9402–0.9405 | 0.0002285 | 2/2 | ratio | tshark_echo |
| failed_calls | 0 | 0 | 0–0 | 0 | 2/2 | count | sipp_csv |
| hangup_causes (16) | 5 | 5 | 5–5 | 0 | 2/2 | count | asterisk_ami_cel |
| pbx_call_ids_correlated | 5 | 5 | 5–5 | 0 | 2/2 | count | asterisk_ami |
| pbx_dtmf_confirmed | 0 | 0 | 0–0 | 0 | 2/2 | count | asterisk_ami |
| pbx_transfer_confirmed | 0 | 0 | 0–0 | 0 | 2/2 | count | asterisk_ami |
| qdisc_drops | 22 | 22 | 22–22 | 0 | 2/2 | count | tc_s_qdisc |
| qdisc_overlimits | 0 | 0 | 0–0 | 0 | 2/2 | count | tc_s_qdisc |
| rtp_packet_loss_pbx_to_uac | 5.962 | 5.962 | 5.946–5.978 | 0.02285 | 2/2 | pct | tshark_pcap_rtp |
| rtp_packet_loss_uac_to_pbx | 0 | 0 | 0–0 | 0 | 2/2 | pct | tshark_pcap_rtp |
| rtp_receiver_jitter_pbx_to_uac | 4.159 | 4.159 | 4.121–4.197 | 0.05378 | 2/2 | ms | tshark_pcap_rtp |
| rtp_receiver_jitter_uac_to_pbx | 4.104 | 4.104 | 4.074–4.135 | 0.04296 | 2/2 | ms | tshark_pcap_rtp |
| rtt_ms | 0.1186 | 0.1186 | 0.1152–0.1221 | 0.004889 | 2/2 | ms | tshark_echo_p50_unique_payload |
| scenario_success_rate | 1 | 1 | 1–1 | 0 | 2/2 | ratio | sipp_csv |
| sip_codes_pbx_to_uac (100) | 5 | 5 | 5–5 | 0 | 2/2 | count | tshark_sip |
| sip_codes_pbx_to_uac (200) | 10 | 10 | 10–10 | 0 | 2/2 | count | tshark_sip |
| sip_retransmits | 0 | 0 | 0–0 | 0 | 2/2 | count | sipp_csv |
| sip_timeouts | 0 | 0 | 0–0 | 0 | 2/2 | count | sipp_csv |
| sipp_cpu_pct_peak | 4.879 | 4.879 | 4.851–4.906 | 0.03846 | 2/2 | pct_one_logical_cpu | procfs |
| sipp_rss_mib_peak | 13.42 | 13.42 | 13.29–13.55 | 0.1878 | 2/2 | MiB | procfs |
| successful_calls | 5 | 5 | 5–5 | 0 | 2/2 | count | sipp_csv |

## Baseline comparison

| Stage / metric | Impaired − baseline median | Unit |
| --- | ---: | --- |
| loss/asterisk_channels_remaining | 0 | count |
| loss/asterisk_cpu_pct_peak | -2.531 | pct_one_logical_cpu |
| loss/asterisk_rss_mib_peak | 0.9062 | MiB |
| loss/call_attempts | 0 | count |
| loss/call_setup_latency_max_ms | 9.5 | ms |
| loss/call_setup_latency_p50_ms | 1.5 | ms |
| loss/call_setup_latency_p95_ms | 9.5 | ms |
| loss/concurrent_calls_peak | 0 | count |
| loss/cps_achieved | -0.0005 | calls_per_sec |
| loss/cps_configured | 0 | calls_per_sec |
| loss/echo_unique_payload_match_rate | -0.05962 | ratio |
| loss/failed_calls | 0 | count |
| loss/pbx_call_ids_correlated | 0 | count |
| loss/pbx_dtmf_confirmed | 0 | count |
| loss/pbx_transfer_confirmed | 0 | count |
| loss/qdisc_drops | 22 | count |
| loss/qdisc_overlimits | 0 | count |
| loss/rtp_packet_loss_pbx_to_uac | 5.962 | pct |
| loss/rtp_packet_loss_uac_to_pbx | 0 | pct |
| loss/rtp_receiver_jitter_pbx_to_uac | -0.2445 | ms |
| loss/rtp_receiver_jitter_uac_to_pbx | -0.2511 | ms |
| loss/rtt_ms | -0.0149 | ms |
| loss/scenario_success_rate | 0 | ratio |
| loss/sip_retransmits | 0 | count |
| loss/sip_timeouts | 0 | count |
| loss/sipp_cpu_pct_peak | 0.003568 | pct_one_logical_cpu |
| loss/sipp_rss_mib_peak | 0.125 | MiB |
| loss/successful_calls | 0 | count |

## Acceptance

| Check | Observed | Threshold | Result |
| --- | ---: | ---: | --- |
| baseline/loss minimum scenario success | 1 | `>= 0.99` | PASS |
| impaired/loss minimum scenario success | 1 | `>= 0.8` | PASS |

## Evidence

- [Run snapshot](snapshot.json)
- [Machine-readable report](report.json)
- [Artifact manifest](artifacts.json)
- [baseline-loss-01](baseline-loss-01/trial.json) · SUCCEEDED
- [baseline-loss-02](baseline-loss-02/trial.json) · SUCCEEDED
- [impaired-loss-01](impaired-loss-01/trial.json) · SUCCEEDED
- [impaired-loss-02](impaired-loss-02/trial.json) · SUCCEEDED

## Interpretation

- Experiments describe the isolated local Asterisk lab. Carrier, production and conversational quality conclusions require separate evidence.
- The seeded netem sequence depends on packet order and the host schedule.
- Qdisc drops may include both configured impairment and queue saturation.
- Setup timings are SIP INVITE to first successful response. Echo RTT requires uniquely matched round-trip payloads.
- RTP loss uses sender-to-receiver identity matching. Jitter is the median of final RFC 3550 estimates across streams.
- CPU utilization is process-based, in units of one logical CPU.
- Fewer than five planned repeats per condition; treat observed spread as preliminary.
