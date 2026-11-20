"use client";

import { useCallback, useEffect, useState } from "react";

const active = new Set(["QUEUED", "RUNNING", "CANCELLING"]);
const sortRuns = (items) => items.filter((item) => item.status === "SUCCEEDED");
const display = (value) => value == null ? "—" : Number(value.toPrecision(5)).toLocaleString();
const short = (id) => id.slice(0, 8);

const metrics = {
  scenario_success_rate: ["Scenario success", "%", 100],
  call_setup_latency_p95_ms: ["SIP setup p95", "ms", 1],
  rtp_packet_loss_uac_to_pbx: ["RTP loss to PBX", "%", 1],
  rtp_receiver_jitter_uac_to_pbx: ["RTP jitter at PBX", "ms", 1],
  rtt_ms: ["RTP echo RTT", "ms", 1],
  qdisc_drops: ["Qdisc drops", "", 1],
};

function Status({ value }) {
  return <span className={`status ${value.toLowerCase()}`}><i />{value.replaceAll("_", " ")}</span>;
}

function ComparisonCards({ groups, stage }) {
  return <div className="cards">{Object.entries(metrics).map(([key, [label, unit, multiplier]]) => {
    const base = groups.baseline?.[stage]?.[key];
    const subject = groups.impaired?.[stage]?.[key];
    const a = base?.median == null ? null : base.median * multiplier;
    const b = subject?.median == null ? null : subject.median * multiplier;
    const scale = Math.max(a ?? 0, b ?? 0, 0.01);
    return <article key={key} className="metric-card">
      <h3>{label}</h3>
      {[["Baseline", a, base, "base"], ...(groups.impaired ? [["Impaired", b, subject, "fault"]] : [])]
        .map(([caption, value, details, kind]) => <div key={kind} className={`measure ${kind}`}>
          <div><span>{caption}</span><strong title={details?.source}>{display(value)} <small>{value == null ? "" : unit}</small></strong></div>
          <div className="track"><div style={{ width: `${100 * (value ?? 0) / scale}%` }} /></div>
        </div>)}
    </article>;
  })}</div>;
}

export default function Workbench() {
  const [token, setToken] = useState("");
  const [draft, setDraft] = useState("");
  const [catalog, setCatalog] = useState(null);
  const [runs, setRuns] = useState([]);
  const [selected, setSelected] = useState("");
  const [run, setRun] = useState(null);
  const [scenario, setScenario] = useState("S0");
  const [profile, setProfile] = useState("");
  const [calls, setCalls] = useState("");
  const [repeats, setRepeats] = useState("");
  const [stage, setStage] = useState("");
  const [other, setOther] = useState("");
  const [comparison, setComparison] = useState(null);
  const [evidence, setEvidence] = useState([]);
  const [tab, setTab] = useState("results");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    const saved = sessionStorage.getItem("callpath.token");
    if (saved) { setToken(saved); setDraft(saved); }
  }, []);

  const request = useCallback(async (path, options = {}, access = token) => {
    const response = await fetch(`/api${path}`, {
      ...options, headers: { Authorization: `Bearer ${access}`, "Content-Type": "application/json" },
      cache: "no-store",
    });
    const body = await response.json().catch(() => null);
    if (!response.ok) {
      const detail = body?.detail;
      throw new Error(typeof detail === "string" ? detail
        : detail?.[0]?.msg || `Request failed (${response.status})`);
    }
    return body;
  }, [token]);

  useEffect(() => {
    if (!token) return;
    let live = true;
    request("/profiles").then((result) => { if (live) setCatalog(result); })
      .catch((problem) => { if (live) setError(problem.message); });
    return () => { live = false; };
  }, [request, token]);

  useEffect(() => {
    if (!token || !catalog) return;
    let live = true;
    const refresh = () => request("/runs").then(({ items }) => {
      if (!live) return;
      setRuns(items);
      setSelected((id) => id || items[0]?.run_id || "");
    }).catch((problem) => { if (live) setError(problem.message); });
    refresh();
    const interval = setInterval(refresh, 2400);
    return () => { live = false; clearInterval(interval); };
  }, [request, token, catalog]);

  useEffect(() => {
    if (!catalog || !selected) return;
    let live = true;
    let interval;
    const refresh = async () => {
      try {
        const result = await request(`/runs/${selected}`);
        if (!live) return;
        setRun(result);
        if (!active.has(result.status)) {
          clearInterval(interval);
          const result = await request(`/runs/${selected}/artifacts`);
          if (live) setEvidence(result.artifacts);
        }
      } catch (problem) { if (live) setError(problem.message); }
    };
    interval = setInterval(refresh, 2000);
    refresh();
    return () => { live = false; clearInterval(interval); };
  }, [catalog, request, selected]);

  async function submit(event) {
    event.preventDefault();
    setError("");
    setBusy(true);
    try {
      const result = await request("/runs", {
        method: "POST",
        body: JSON.stringify({
          scenario_id: scenario, target_id: catalog.target_id,
          impairment_profile_id: profile || null, repeats: repeats ? Number(repeats) : null,
          overrides: calls ? { calls: Number(calls) } : {},
        }),
      });
      setRuns((previous) => [{ ...result, scenario_id: scenario, created_at: new Date().toISOString() }, ...previous]);
      choose(result.run_id);
    } catch (problem) { setError(problem.message); }
    finally { setBusy(false); }
  }

  function choose(id) {
    if (id === selected) return;
    setSelected(id); setRun(null); setEvidence([]); setStage(""); setTab("results");
    setOther(""); setComparison(null); setError("");
  }

  async function cancel() {
    try {
      const outcome = await request(`/runs/${run.run_id}/cancel`, { method: "POST" });
      setRun({ ...run, status: outcome.status });
    } catch (problem) { setError(problem.message); }
  }

  async function compare(event) {
    event.preventDefault();
    setError("");
    setComparison(null);
    try {
      const result = await request(`/runs/compare?run_id=${run.run_id}&baseline_run_id=${other}`);
      setComparison(result);
    } catch (problem) { setError(problem.message); }
  }

  function unlock(event) {
    event.preventDefault();
    const access = draft.trim();
    sessionStorage.setItem("callpath.token", access);
    setError("");
    setToken(access);
  }

  function lock() {
    sessionStorage.removeItem("callpath.token");
    setToken(""); setDraft(""); setCatalog(null); setRuns([]); setSelected("");
    setRun(null); setError("");
  }

  const groups = run?.summary?.aggregates || {};
  const stages = Object.keys(groups.baseline || {});
  const current = stages.includes(stage) ? stage : stages[0];

  return <>
    <header className="top">
      <a className="brand" href="/" aria-label="CallPath home"><span className="mark" aria-hidden>╱╲</span> CallPath</a>
      <div className="top-right"><span className="target">Local Asterisk</span>
        {catalog && <button className="quiet" onClick={lock}>Lock</button>}
      </div>
    </header>
    <main className={catalog ? "workbench" : "locked"}>
      {error && <div className="notice" role="alert">{error}</div>}
      {!catalog ? <form className="login" onSubmit={unlock}>
        <h1>Connect to CallPath</h1>
        <p>Enter the token configured for the local API.</p>
        <label>API token<input type="password" value={draft} onChange={(event) => setDraft(event.target.value)} required autoComplete="off" /></label>
        <button type="submit" className="primary">Connect</button>
      </form> : <>
        <div className="heading"><h1>Experiment workbench</h1></div>
        <div className="layout">
          <aside>
            <form className="panel launch" onSubmit={submit}>
              <h2>New run</h2>
              <label>Scenario<select value={scenario} onChange={(event) => setScenario(event.target.value)}>
                {Object.entries(catalog.scenarios).map(([id, label]) => <option key={id} value={id}>{id} · {label}</option>)}
              </select></label>
              <label>Impairment<select value={profile} onChange={(event) => setProfile(event.target.value)}>
                <option value="">Scenario default</option>
                {catalog.impairment_profiles.map((item) => <option key={item} value={item}>{item}</option>)}
              </select></label>
              <div className="split">
                <label>Calls<input type="number" min="1" max="1500" placeholder="Default" value={calls} onChange={(event) => setCalls(event.target.value)} /></label>
                <label>Repeats<input type="number" min="1" max="15" placeholder="Default" value={repeats} onChange={(event) => setRepeats(event.target.value)} /></label>
              </div>
              <button type="submit" className="primary" disabled={busy}>{busy ? "Queueing…" : "Queue run"}</button>
            </form>
            <section className="panel history" aria-label="Run history">
              <h2>Run history</h2>
              {!runs.length && <p className="muted">No experiments queued.</p>}
              {runs.map((item) => <button key={item.run_id} className="history-item"
                aria-pressed={selected === item.run_id} onClick={() => choose(item.run_id)}>
                <span><strong>{item.scenario_id}</strong><small>{short(item.run_id)}</small></span><Status value={item.status} />
              </button>)}
            </section>
          </aside>
          <section className="panel run" aria-label="Run details">
            {!run ? <div className="empty"><h2>{selected ? "Loading run…" : "Run results"}</h2>
              {!selected && <p>Queue an experiment to collect SIP, RTP and cleanup evidence.</p>}</div> : <>
              <div className="run-heading">
                <div><p className="run-id">{run.run_id}</p><h2>{run.scenario_id} · {catalog.scenarios[run.scenario_id]}</h2></div>
                <div className="run-actions"><Status value={run.status} />
                  {["QUEUED", "RUNNING"].includes(run.status) && <button className="quiet" onClick={cancel}>Cancel run</button>}
                </div>
              </div>
              {run.error && <p className="notice">{run.error}</p>}
              {!run.summary ? <div className="empty"><p>{active.has(run.status) ? "Waiting for the lab worker to publish evidence." : "No run report was published."}</p></div> : <>
                <nav className="tabs" aria-label="Run sections">
                  {["results", "evidence", "compare"].map((item) => <button key={item} aria-pressed={tab === item}
                    onClick={() => setTab(item)}>{item}</button>)}
                  <span className="cleanup">{run.summary.cleanup.verified ? "Cleanup verified" : "Cleanup unverified"}</span>
                </nav>
                {tab === "results" && <div className="content">
                  {stages.length > 1 && <label className="stage">Stage<select value={current} onChange={(event) => setStage(event.target.value)}>
                    {stages.map((item) => <option key={item}>{item}</option>)}
                  </select></label>}
                  {current && <ComparisonCards groups={groups} stage={current} />}
                  <h3>Acceptance checks</h3>
                  <div className="scroll"><table><thead><tr><th>Check</th><th>Observed</th><th>Threshold</th><th>Result</th></tr></thead>
                    <tbody>{run.summary.checks.map((item) => <tr key={item.check}>
                      <td>{item.check}</td><td>{display(item.observed)}</td>
                      <td>{item.operator} {item.threshold}</td><td><Status value={item.status} /></td>
                    </tr>)}</tbody></table></div>
                </div>}
                {tab === "evidence" && <div className="content">
                  <h3>Artifact manifest</h3>
                  <p className="muted">Files are stored on the worker under this run ID.</p>
                  <div className="scroll"><table><thead><tr><th>Path</th><th>Kind</th><th>Bytes</th><th>SHA-256</th></tr></thead><tbody>
                    {evidence.map((item) => <tr key={item.path}><td>{item.path}</td><td>{item.type}</td>
                      <td>{item.size_bytes.toLocaleString()}</td><td><code title={item.sha256}>{item.sha256.slice(0, 16)}…</code></td></tr>)}
                  </tbody></table></div>
                </div>}
                {tab === "compare" && <div className="content">
                  <form className="compare-form" onSubmit={compare}>
                    <label>Baseline run<select value={other} onChange={(event) => setOther(event.target.value)} required>
                      <option value="">Choose a completed run</option>
                      {sortRuns(runs).filter((item) => item.run_id !== selected).map((item) => <option key={item.run_id} value={item.run_id}>
                        {item.scenario_id} · {short(item.run_id)}
                      </option>)}
                    </select></label><button className="primary" disabled={run.status !== "SUCCEEDED" || !other}>Compare</button>
                  </form>
                  {comparison && (comparison.compatible ? <div className="scroll"><table>
                    <thead><tr><th>Stage / metric</th><th>Baseline median</th><th>Run median</th><th>Delta</th></tr></thead>
                    <tbody>{Object.entries(comparison.deltas).filter(([, item]) => item.median_delta != null).map(([key, item]) => <tr key={key}>
                      <td>{key}</td><td>{display(item.baseline.median)}</td><td>{display(item.subject.median)}</td>
                      <td>{display(item.median_delta)} {item.subject.unit}</td>
                    </tr>)}</tbody>
                  </table></div> : <p className="notice">{comparison.warnings.join(" · ")}</p>)}
                </div>}
              </>}
            </>}
          </section>
        </div>
      </>}
    </main>
  </>;
}
