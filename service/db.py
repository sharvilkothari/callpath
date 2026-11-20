"""PostgreSQL transactions for the lab queue."""
from contextlib import contextmanager
from datetime import datetime, timezone
import os

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb


@contextmanager
def connect():
    with psycopg.connect(os.environ["CALLPATH_DB_URL"], row_factory=dict_row,
                         connect_timeout=5, options="-c statement_timeout=15000") as conn:
        yield conn


def claim(conn, token):
    return conn.execute("""
        WITH next AS (
            SELECT run_id FROM test_runs
            WHERE status IN ('QUEUED','CANCELLING') AND lease_token IS NULL AND started_at IS NULL
            ORDER BY created_at
            FOR UPDATE SKIP LOCKED LIMIT 1
        )
        UPDATE test_runs AS run
        SET status = CASE WHEN run.status = 'CANCELLING' THEN 'CANCELLING' ELSE 'RUNNING' END,
            lease_token = %s, lease_until = now() + interval '30 seconds', started_at = now()
        FROM next WHERE run.run_id = next.run_id
        RETURNING run.run_id, run.status, run.request
    """, (token,)).fetchone()


def heartbeat(conn, run_id, token):
    row = conn.execute("""
        UPDATE test_runs SET lease_until = now() + interval '30 seconds'
        WHERE run_id = %s AND lease_token = %s RETURNING status
    """, (run_id, token)).fetchone()
    return row["status"] if row else None


def expired(conn):
    return conn.execute("""
        SELECT run_id, lease_token FROM test_runs
        WHERE status IN ('RUNNING','CANCELLING') AND lease_until < now()
    """).fetchall()


def finalize(conn, run_id, token, status, snapshot=None, report=None, artifacts=(), events=(),
             error=None):
    updated = conn.execute("""
        UPDATE test_runs SET status = %s, snapshot = %s, summary = %s, error = %s,
            ended_at = now(), lease_token = NULL, lease_until = NULL
        WHERE run_id = %s AND lease_token = %s RETURNING run_id
    """, (status, Jsonb(snapshot) if snapshot else None, Jsonb(report) if report else None,
          error, run_id, token)).fetchone()
    if not updated:
        return False
    rows = []
    for trial in (report or {}).get("trials", []):
        for metric, record in trial.get("metrics", {}).items():
            value = record["value"]
            rows.append((run_id, trial["id"], metric, value if isinstance(value, (int, float)) else None,
                         Jsonb(value) if isinstance(value, dict) else None,
                         record["unit"], record["source"], record["direction"],
                         record["availability"], record.get("reason")))
    with conn.cursor() as cursor:
        if rows:
            cursor.executemany("""
                INSERT INTO metric_samples (run_id,trial_id,metric_name,value,breakdown,unit,
                    source,direction,availability,reason) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, rows)
        if artifacts:
            cursor.executemany("""
                INSERT INTO artifacts (run_id,artifact_type,path,sha256,size_bytes)
                VALUES (%s,%s,%s,%s,%s)
            """, [(run_id, row["type"], row["path"], row["sha256"], row["size_bytes"])
                  for row in artifacts])
        if events:
            params = [(run_id, trial_id, item["call_id"], item.get("eventname", item["event"]),
                       item.get("cause"), datetime.fromtimestamp(item["observed_at"], timezone.utc),
                       Jsonb(item)) for trial_id, item in events if item.get("call_id")]
            cursor.executemany("""
                INSERT INTO call_events (run_id,trial_id,call_id,event_type,cause,occurred_at,details)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, params)
    return True
