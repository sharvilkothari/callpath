# CallPath verification

The CLI suite ran real SIPp and Asterisk calls in isolated Linux containers. Each linked run includes its snapshot, per-trial evidence, PCAPs where available, and a verified SHA-256 manifest.

| Scenario | Result |
| --- | --- |
| [S0](evidence/egress/f21b71952e67f1be019e17be8ae95b4e/report.md) | One successful SIP dialog, correlated PBX events, and bidirectional PCMU. |
| [S1](evidence/egress/72142963545ae7f5e32923f541c1db91/report.md) | Five baseline repeats passed the configured success and setup latency spread checks. |
| [S2](evidence/egress/2b4aacd30611ae2dc335506a0c7e51b5/report.md) | The 2, 5 and 10 CPS stages completed and published SIP and resource metrics. |
| [S3](evidence/egress/af4330488e66e827e027aafcd143a2e5/report.md) | 240 successful calls at 2 offered CPS with zero remaining PBX channels. |
| [S4](evidence/egress/199c372be2280c31924d366ff8b2ca31/report.md) | Five trials per condition. Median SIP setup p95 increased 91 ms with an 80 ms delay profile. |
| [S5](evidence/egress/ae184d1adeadc63ba85fbead95b6c93a/report.md) | Five trials per condition. Forward RTP loss increased 7.46 percentage points with 8% configured loss. The reverse change was 0.00 points. |
| [S6](evidence/egress/1c46f765a737da9b26fa08dbc724d511/report.md) | Five DTMF and five blind transfer dialogs passed SIPp and PBX confirmation. |
| [S7](evidence/egress/edf2ce69eb170dd4854d003a84fa1a15/report.md) | Five trials per condition. Uniquely matched echo RTT increased 81.4 ms with bidirectional delay. |

[Independent S4 reference](evidence/egress/23440a2b7f1fde112849808470c1db61/report.md) and [compatibility-checked comparison](evidence/egress-comparison.json).

[Ubuntu IFB ingress run](evidence/ingress/5ab2924c5630edf354fbef54c92e36b8/report.md). Five trials per condition at 8% configured RTP loss. Median loss increased 7.24 percentage points toward the PBX and 7.56 on the return path.

[Reverse-path burst loss run](evidence/burst/569b36d08c7ff06eed2242c2d878bcfb/report.md). Measured loss increased 5.96 percentage points in the selected direction.

## Lifecycle and service

The timeout, cancel, and forced-container-kill runs each recorded verified teardown. The kill was recovered by the janitor and preserved a teardown proof.

- [TIMED_OUT](evidence/lifecycle/502143dece6b8ecee48eb6646019aa49/report.md)
- [CANCELLED](evidence/lifecycle/53e8fca165711c9aaafbad20c962117b/report.md)
- [Forced termination recovery](evidence/lifecycle/f6d7ff7582e9a153cb1b9e1f26527eee/report.md)

The API integration exercised bearer authentication, bounded requests, queued and active cancellation, worker execution, timestamp-filtered metrics, artifacts, and comparison. The worker was also killed with an active lease and recovered the run after lease expiry.

- [HTTP integration log](evidence/service-tests.log)
- [Expired lease recovery log](evidence/lease-test.log)
- [CLI lifecycle log](evidence/lifecycle.log)
- [Browser integration log](evidence/browser-linux.log)
- [Desktop dashboard](evidence/workbench-desktop.png)
- [Mobile dashboard](evidence/workbench-mobile.png)

Egress tests used the Docker Desktop LinuxKit 6.10.14 kernel. IFB testing used an Ubuntu 24.04 VM with Linux 6.8.0-147-generic. Both used Asterisk 22.5.2, SIPp 3.7.7, iproute2 6.19.0, tcpdump 4.99.6 and tshark 4.6.4. The test environment covers macOS Docker Desktop and Ubuntu Linux.
