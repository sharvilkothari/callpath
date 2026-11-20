"""Authenticated local HTTP interface to the durable run queue."""
from datetime import datetime
import os
import secrets
import uuid

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from psycopg.types.json import Jsonb

from callpath.model import PROFILES, SCENARIOS, TERMINAL
from callpath.report import compare_values, compatibility_warnings
from callpath.storage import ID
from service.contracts import RunRequest
from service.db import connect

bearer = HTTPBearer(auto_error=False)


def authorized(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    expected = os.environ.get("CALLPATH_API_TOKEN", "")
    if len(expected) < 24:
        raise HTTPException(503, "Configure a local API token of at least 24 characters")
    if not credentials or not secrets.compare_digest(credentials.credentials.encode(), expected.encode()):
        raise HTTPException(401, "Valid bearer token required", headers={"WWW-Authenticate": "Bearer"})


app = FastAPI(title="CallPath", version="1.0", dependencies=[Depends(authorized)],
              docs_url=None, redoc_url=None, openapi_url=None)


def checked_id(value):
    if not ID.fullmatch(value):
        raise HTTPException(400, "Malformed run ID")
    return value


def get_run(conn, run_id, lock=False):
    suffix = " FOR UPDATE" if lock else ""
    row = conn.execute("""
        SELECT run_id, scenario_id, target_id, impairment_profile_id, status, request,
            snapshot, summary, error, created_at, started_at, ended_at
        FROM test_runs WHERE run_id = %s
    """ + suffix, (checked_id(run_id),)).fetchone()
    if row is None:
        raise HTTPException(404, "Run not found")
    return row


@app.get("/profiles")
def profiles():
    return {"scenarios": SCENARIOS, "impairment_profiles": list(PROFILES), "target_id": "ast_local"}


@app.post("/runs", status_code=201)
def enqueue(request: RunRequest):
    if request.scenario_id not in SCENARIOS:
        raise HTTPException(404, "Scenario not found")
    if request.target_id != "ast_local":
        raise HTTPException(404, "Target not found")
    if request.impairment_profile_id is not None and request.impairment_profile_id not in PROFILES:
        raise HTTPException(404, "Impairment profile not found")
    run_id = uuid.uuid4().hex
    with connect() as conn:
        conn.execute("""
            INSERT INTO test_runs (run_id,scenario_id,target_id,impairment_profile_id,status,request)
            VALUES (%s,%s,%s,%s,'QUEUED',%s)
        """, (run_id, request.scenario_id, request.target_id, request.impairment_profile_id,
              Jsonb(request.model_dump(exclude_none=True))))
    return {"run_id": run_id, "status": "QUEUED"}


@app.get("/runs")
def runs(limit: int = Query(50, ge=1, le=100)):
    with connect() as conn:
        rows = conn.execute("""
            SELECT run_id, scenario_id, status, created_at, started_at, ended_at, error
            FROM test_runs ORDER BY created_at DESC LIMIT %s
        """, (limit,)).fetchall()
    return {"items": rows}


@app.get("/runs/compare")
def compare(run_id: str, baseline_run_id: str):
    if run_id == baseline_run_id:
        raise HTTPException(400, "Choose two runs")
    with connect() as conn:
        a = get_run(conn, baseline_run_id)
        b = get_run(conn, run_id)
    if a["status"] != "SUCCEEDED" or b["status"] != "SUCCEEDED":
        raise HTTPException(409, "Wait for both runs to complete")
    left, right = a["snapshot"], b["snapshot"]
    if not left or not right:
        raise HTTPException(409, "Both runs need snapshots")
    warnings = compatibility_warnings(right, left)
    if warnings:
        return {"compatible": False, "warnings": warnings, "deltas": {}}
    baseline = a["summary"]["aggregates"].get("baseline", {})
    groups = b["summary"]["aggregates"]
    current = groups.get("impaired", groups.get("baseline", {}))
    return {"compatible": True, "warnings": [], "deltas": compare_values(baseline, current)}


@app.get("/runs/{run_id}")
def show(run_id: str):
    with connect() as conn:
        return get_run(conn, run_id)


@app.post("/runs/{run_id}/cancel", status_code=202)
def cancel(run_id: str):
    with connect() as conn:
        run = get_run(conn, run_id, lock=True)
        if run["status"] in TERMINAL:
            raise HTTPException(409, "Run is terminal")
        conn.execute("UPDATE test_runs SET status = 'CANCELLING' WHERE run_id = %s", (run_id,))
    return {"run_id": run_id, "status": "CANCELLING"}


@app.get("/runs/{run_id}/metrics")
def metrics(run_id: str, metric_name: str | None = None,
            start: datetime | None = None, end: datetime | None = None,
            limit: int = Query(5000, ge=1, le=10000)):
    if any(item is not None and item.tzinfo is None for item in (start, end)):
        raise HTTPException(400, "Metric windows require offset-aware timestamps")
    if start is not None and end is not None and start > end:
        raise HTTPException(400, "Metric window start must precede end")
    with connect() as conn:
        get_run(conn, run_id)
        rows = conn.execute("""
            SELECT trial_id, metric_name, value, breakdown, unit, source, direction,
                availability, reason, recorded_at
            FROM metric_samples WHERE run_id = %s
                AND (%s::text IS NULL OR metric_name = %s)
                AND (%s::timestamptz IS NULL OR recorded_at >= %s)
                AND (%s::timestamptz IS NULL OR recorded_at <= %s)
            ORDER BY id LIMIT %s
        """, (run_id, metric_name, metric_name, start, start, end, end, limit + 1)).fetchall()
    return {"items": rows[:limit], "truncated": len(rows) > limit}


@app.get("/runs/{run_id}/artifacts")
def artifacts(run_id: str):
    with connect() as conn:
        get_run(conn, run_id)
        items = conn.execute("""
            SELECT artifact_type AS type,path,sha256,size_bytes FROM artifacts
            WHERE run_id = %s ORDER BY path
        """, (run_id,)).fetchall()
    return {"artifacts": items}
