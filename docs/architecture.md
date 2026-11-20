# CallPath architecture and metrics

Each run uses one disposable Linux container and an exclusive artifact-directory lock. The runner starts as an unprivileged account. A root-owned helper checks the dedicated caller and accepts only fixed actions with bounded numeric profiles. It cannot take a custom executable, scenario path, interface, target, shell fragment or arbitrary traffic-control arguments. SIPp and Asterisk enter their lab namespaces and drop privileges before running. The privileged capture launcher opens packet sockets on fixed interfaces and tcpdump drops privileges with `-Z`.

```text
              Linux container with no external network
        cp-sipp                                  cp-pbx
   SIPp 10.200.1.2    cp-veth-sipp ↔ cp-veth-pbx    Asterisk 10.200.1.3
        │   │                                       │   │
      TX    RX                                     RX   TX
   mirror capture                              capture mirror

   Egress shape    netem on the designated sender veth
   Ingress shape   receiver ingress redirect → IFB → netem
```

The generator sends SIP UDP to port 5060 and negotiates G.711 µ-law at 8 kHz with 20 ms, 160-byte RTP payloads. The dialplan loops media back locally. The PBX uses RTP ports 10000–10199. A classful qdisc can use UDP port filters to send only signaling or media through netem. Both directions are configured independently. Profile bounds and the seed are recorded even for a zero-fault baseline. Seeded behavior depends on packet order and scheduling.

The sender copy is a veth mirror taken at clsact egress before the root qdisc. The peer capture sees delivered packets, or IFB egress when that receiver uses ingress shaping. All four capture streams must report complete capture counts and zero kernel capture drops before their data are used for the affected direction. Filtered UDP ports plus PCMU payload type identify RTP. Each stream is grouped by UDP port pair and SSRC. Loss uses missing unique sequence/timestamp pairs from the sender. Jitter is the median of the final per-stream RFC 3550 estimator, using arrival order and the 8 kHz RTP clock. Echo RTT matches unique raw PCMU payloads through reversed ports and uses same-host packet timestamps. It includes PBX processing time and both paths.

SIPp's outgoing and completed-call counters give attempt and success rates. SIPp response-time traces measure INVITE to the first 2xx in the defined scenario and supply nearest-rank p50, p95 and max. Concurrent call peaks use one-second SIPp samples. SIP status codes are counts of captured received messages, including messages observed more than once. AMI gives hangup causes and DTMF results. CEL and AMI channel records are associated with SIP Call-ID through the dialplan correlation event and Asterisk channel IDs. Resource measurements use process CPU deltas and resident memory from procfs. UDP socket tables and final PBX channels are retained as artifacts.

A normal, cancelled or timed-out trial closes captures, collects counters and removes its owned links and namespaces. The helper verifies that names and processes are gone. Its lease tracks owned resources and lets a subsequent helper remove interrupted setup. If the container itself is killed, the startup janitor uses the same Docker engine's container inventory and recorded unique container name to verify container teardown. Unknown ownership or unverified removal produces `CLEANUP_FAILED`.

The optional PostgreSQL worker claims queued records with `FOR UPDATE SKIP LOCKED` and renews a timed lease. It materializes reports, events, metrics and manifest metadata after the lab has completed. Each artifact directory supports one worker and one active lab lock. The API and Next.js dashboard have no Docker socket and publish to loopback only. The worker is the local execution boundary. Raw PCAPs are kept in the chosen artifact directory.

Results describe this standalone local lab. Production carrier validation, PSTN routing, subjective voice quality, and the specification's future TLS, registration, codec negotiation and external-sandbox extensions require separate work.

- [SIPp statistics](https://sipp.readthedocs.io/en/latest/statistics.html)
- [SIPp RTP streaming](https://sipp.readthedocs.io/en/latest/scenarios/actions.html#media-rtp-commands)
- [Asterisk AMI CEL event](https://docs.asterisk.org/Latest_API/API_Documentation/AMI_Events/CEL/)
- [Linux netem](https://www.man7.org/linux/man-pages/man8/netem.8.html)
- [RFC 3550 RTP](https://www.rfc-editor.org/rfc/rfc3550)
