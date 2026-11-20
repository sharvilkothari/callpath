CREATE TABLE IF NOT EXISTS scenarios (
    id text PRIMARY KEY,
    version text NOT NULL,
    xml_sha256 text,
    params jsonb NOT NULL
);
CREATE TABLE IF NOT EXISTS target_profiles (
    id text PRIMARY KEY,
    host inet NOT NULL,
    port int NOT NULL,
    transport text NOT NULL,
    allowlisted boolean NOT NULL
);
CREATE TABLE IF NOT EXISTS impairment_profiles (
    id text PRIMARY KEY,
    delay_ms int NOT NULL,
    jitter_ms int NOT NULL,
    loss_pct double precision NOT NULL,
    queue_limit int NOT NULL,
    burst_cfg jsonb,
    seed bigint NOT NULL,
    params jsonb NOT NULL
);
CREATE TABLE IF NOT EXISTS test_runs (
    run_id text PRIMARY KEY CHECK (run_id ~ '^[a-f0-9]{32}$'),
    scenario_id text NOT NULL REFERENCES scenarios(id),
    target_id text NOT NULL REFERENCES target_profiles(id),
    impairment_profile_id text REFERENCES impairment_profiles(id),
    baseline_run_id text REFERENCES test_runs(run_id),
    status text NOT NULL CHECK (status IN (
        'QUEUED', 'RUNNING', 'CANCELLING', 'SUCCEEDED', 'FAILED',
        'TIMED_OUT', 'CANCELLED', 'CLEANUP_FAILED')),
    request jsonb NOT NULL,
    snapshot jsonb,
    summary jsonb,
    error text,
    lease_token text,
    lease_until timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    started_at timestamptz,
    ended_at timestamptz
);
CREATE TABLE IF NOT EXISTS metric_samples (
    id bigserial PRIMARY KEY,
    run_id text NOT NULL REFERENCES test_runs(run_id) ON DELETE CASCADE,
    trial_id text NOT NULL,
    metric_name text NOT NULL,
    value double precision,
    breakdown jsonb,
    unit text NOT NULL,
    source text NOT NULL,
    direction text NOT NULL,
    availability text NOT NULL,
    reason text,
    recorded_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS call_events (
    id bigserial PRIMARY KEY,
    run_id text NOT NULL REFERENCES test_runs(run_id) ON DELETE CASCADE,
    trial_id text NOT NULL,
    call_id text NOT NULL,
    event_type text NOT NULL,
    sip_code int,
    cause text,
    occurred_at timestamptz NOT NULL,
    details jsonb NOT NULL
);
CREATE TABLE IF NOT EXISTS artifacts (
    id bigserial PRIMARY KEY,
    run_id text NOT NULL REFERENCES test_runs(run_id) ON DELETE CASCADE,
    artifact_type text NOT NULL,
    path text NOT NULL,
    sha256 text NOT NULL,
    size_bytes bigint NOT NULL,
    UNIQUE (run_id, path)
);
CREATE INDEX IF NOT EXISTS idx_test_runs_status_created ON test_runs(status, created_at);
CREATE INDEX IF NOT EXISTS idx_metric_samples_run_metric ON metric_samples(run_id, metric_name);
CREATE INDEX IF NOT EXISTS idx_call_events_run_time ON call_events(run_id, occurred_at);
CREATE INDEX IF NOT EXISTS idx_artifacts_run ON artifacts(run_id);

INSERT INTO scenarios VALUES
    ('S0', '1.0', NULL, '{"default_repeats":1}'),
    ('S1', '1.0', NULL, '{"default_repeats":5}'),
    ('S2', '1.0', NULL, '{"default_repeats":1}'),
    ('S3', '1.0', NULL, '{"default_repeats":1}'),
    ('S4', '1.0', NULL, '{"default_repeats":5}'),
    ('S5', '1.0', NULL, '{"default_repeats":5}'),
    ('S6', '1.0', NULL, '{"default_repeats":1}'),
    ('S7', '1.0', NULL, '{"default_repeats":5}')
ON CONFLICT DO NOTHING;

INSERT INTO target_profiles VALUES ('ast_local', '10.200.1.3', 5060, 'udp', true)
ON CONFLICT DO NOTHING;

INSERT INTO impairment_profiles VALUES
    ('baseline', 0, 0, 0, 1000, NULL, 42, '{}'),
    ('delay', 80, 20, 0, 1000, NULL, 42, '{"delay_ms":80,"jitter_ms":20}'),
    ('loss', 0, 0, 1, 1000, NULL, 42, '{"loss_pct":1}'),
    ('burst', 0, 0, 0, 1000, '{"start_pct":1,"end_pct":25}', 42,
        '{"burst_start_pct":1,"burst_end_pct":25}'),
    ('echo', 40, 10, 0, 1000, NULL, 42,
        '{"delay_ms":40,"jitter_ms":10,"traffic":"rtp","path":"both"}')
ON CONFLICT DO NOTHING;
