# CallPath

CallPath runs reproducible SIP and RTP experiments against an isolated Asterisk PBX. The Linux runner connects SIPp and Asterisk over a private veth pair, runs the same load with and without impairment, and writes source-labeled metrics with the raw evidence. The optional FastAPI, PostgreSQL and Next.js workbench queues the same experiments locally.

## Run the lab

Use Docker Engine on Linux or Docker Desktop with a compatible Linux kernel. The CLI runs the lab in a disposable container with networking disabled at the container boundary. Use Python 3.11+ on the host for reading reports and running the worker. If Docker requires sudo, pass the intended non-root file owner as `CALLPATH_UID` and `CALLPATH_GID`.

```sh
./lab build
./lab doctor
./lab run S0
./lab run S4 --traffic sip --path both
./lab run S5 --traffic rtp --loss-pct 8 --seed 42
```

The default artifact directory is `artifacts/`. Set `CALLPATH_ARTIFACTS` to a Docker-shareable host directory. On macOS, a temporary directory can be used when Docker Desktop lacks access to your Documents folder.

```sh
export CALLPATH_ARTIFACTS="$(mktemp -d /tmp/callpath.XXXXXX)"
./lab doctor
./lab run S0
```

Ingress mode requires IFB support in the Linux host or VM. The Docker Desktop LinuxKit kernel used during verification supports egress shaping and lacks IFB. On Ubuntu, if IFB is modular, load it in the Linux host or guest before running the ingress test.

```sh
sudo modprobe ifb
./lab doctor --placement ingress --path both --traffic rtp
./lab run S5 --placement ingress --path both --traffic rtp --loss-pct 8
```

| Scenario | Lab flow |
| --- | --- |
| S0 | One call with SIP, RTP and PBX event capture |
| S1 | Five low-rate baseline repeats with a setup-latency spread check |
| S2 | Three isolated stages at 2, 5 and 10 calls per second |
| S3 | A two-minute offered-load soak with a post-run open-channel check |
| S4 | Five baseline and five delay/jitter repeats |
| S5 | Five baseline and five seeded loss repeats |
| S6 | SIP INFO DTMF with PBX confirmation and blind REFER with a successful final NOTIFY and destination confirmation |
| S7 | PCMU echo with sender/receiver loss, jitter and uniquely matched payload RTT |

`./lab run --help` lists load overrides and the delay, jitter, random and burst loss, duplication, reordering, queue limit, seed, direction and traffic controls. S4, S5 and S7 run their own matching baselines automatically. To compare separate compatible runs, use the same scenario, load, host, media and shaping placement with `--baseline-only` on the reference.

```sh
./lab show RUN_ID
./lab metrics RUN_ID
./lab artifacts RUN_ID
./lab compare IMPAIRED_RUN_ID BASELINE_RUN_ID
./lab cancel RUN_ID
./lab janitor
./lab prune --older-than-days 14
```

The directory for each run contains a write-once `snapshot.json`, trial inputs and results, SIPp logs and RTT traces, four PCAPs per trial, Asterisk events, qdisc counters, resource and socket telemetry, `report.json`, `report.md`, and a SHA-256 artifact manifest. A run can finish successfully while an acceptance check fails, such as when measured SIP success falls below the scenario threshold. Missing or untrustworthy data appear as null with source and availability details. Use `prune --apply` to delete the terminal local artifact directories listed by the preview.

## Start the local workbench

Build the lab image first. Create a private `.env` with random hex credentials, then start the local services.

```sh
umask 077
printf 'CALLPATH_API_TOKEN=%s\nCALLPATH_DB_PASSWORD=%s\n' \
  "$(openssl rand -hex 24)" "$(openssl rand -hex 24)" > .env
docker compose up --build -d
```

In another terminal, use the same artifact directory as the CLI and start the worker. On macOS, set `CALLPATH_ARTIFACTS` to a Docker-shareable path before starting the worker. The worker requires access to the local Docker engine.

```sh
python3 -m venv .venv
.venv/bin/pip install -r service/requirements.txt
set -a
. ./.env
set +a
export CALLPATH_DB_URL="postgresql://callpath:${CALLPATH_DB_PASSWORD}@127.0.0.1:${CALLPATH_DB_PORT:-55432}/callpath"
.venv/bin/python -m service.worker
```

Open the dashboard at [http://127.0.0.1:3042](http://127.0.0.1:3042) and enter `CALLPATH_API_TOKEN`. It supports queueing, status and cancellation, per-stage baseline and impairment results, acceptance checks, artifact manifests, and comparisons between compatible runs. Use `docker compose down` to stop the services and keep the PostgreSQL volume.

### HTTP API

The API listens on host loopback port 8042 by default. Pass `Authorization: Bearer TOKEN` on each request. The only target ID is `ast_local`.

| Method | Path | Response |
| --- | --- | --- |
| GET | `/profiles` | Scenario and impairment profile IDs |
| POST | `/runs` | 201 with a queued run ID |
| GET | `/runs` | Recent runs |
| GET | `/runs/{id}` | Status, snapshot, timestamps and report |
| POST | `/runs/{id}/cancel` | 202 with cancellation requested |
| GET | `/runs/{id}/metrics` | Scalar and breakdown samples, filterable by `metric_name`, `start` and `end` |
| GET | `/runs/{id}/artifacts` | Relative paths, sizes, types and hashes |
| GET | `/runs/compare?run_id=…&baseline_run_id=…` | Compatibility and median deltas |

Example request body

```json
{
  "scenario_id": "S5",
  "target_id": "ast_local",
  "impairment_profile_id": "loss",
  "overrides": { "calls": 10, "traffic": "rtp", "loss_pct": 8 },
  "repeats": 5
}
```

## Implementation and evidence

- [Architecture and metric definitions](docs/architecture.md)
- [Verification and retained run evidence](VERIFICATION.md)

Run unit tests with `python3 -m unittest discover -s tests`. With the local services and worker running, `CALLPATH_API_TOKEN` exported, and a test database selected, run `python3 tests/service_integration.py` for the HTTP contract. The CLI integration harness uses real SIPp, Asterisk, tcpdump, tshark and netem, and checks accepted measurements, cleanup and artifact checksums.

```sh
export CALLPATH_ARTIFACTS="$(mktemp -d /tmp/callpath-test.XXXXXX)"
./tests/integration.sh full
./tests/integration.sh lifecycle
./tests/integration.sh ingress
```
