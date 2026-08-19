import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getStepsForTestCase, runTestCase, getTestRuns, getRunDetail, getChangeEvents } from "../api";
export default function TestCaseDetail() {
  const { id } = useParams();
  const [steps, setSteps] = useState([]);
  const [runs, setRuns] = useState([]);
  const [changeEvents, setChangeEvents] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [runningTest, setRunningTest] = useState(false);
  const [runMessage, setRunMessage] = useState("");
  const [selectedRun, setSelectedRun] = useState(null);
  const [selectedRunLoading, setSelectedRunLoading] = useState(false);

  const token = localStorage.getItem("token");
  const navigate = useNavigate();

    const loadData = () => {
    setLoading(true);
    Promise.all([
      getStepsForTestCase(token, id),
      getTestRuns(token, id),
      getChangeEvents(token, id)
    ])
      .then(([stepsRes, runsRes, changesRes]) => {
        setSteps(stepsRes.data);
        setRuns(runsRes.data);
        setChangeEvents(changesRes.data);
      })
      .catch(() => setError("Failed to load test case data from server"))
      .finally(() => setLoading(false));
  };
  useEffect(() => {
    loadData();
  }, [token, id]);

  // Dynamic poll interval during test playback
  useEffect(() => {
    if (!runningTest) return;
    const interval = setInterval(async () => {
      try {
        const res = await getTestRuns(token, id);
        setRuns(res.data);
        const latestRun = res.data[0];
        if (latestRun && latestRun.status !== "running") {
          setRunningTest(false);
          getChangeEvents(token, id).then((res) => setChangeEvents(res.data)).catch(() => {});
          setRunMessage(
            latestRun.status === "passed"
              ? `Regression Run #${latestRun.id} passed (${latestRun.steps_passed}/${latestRun.steps_total} steps in ${latestRun.duration_ms}ms)`
              : `Regression Run #${latestRun.id} failed: ${latestRun.error_message || "Assertion / Element locator timeout"}`
          );
        }
      } catch (e) {}
    }, 2000);
    return () => clearInterval(interval);
  }, [runningTest, token, id]);

  const handleRunTest = async () => {
    setRunningTest(true);
    setRunMessage("Dispatching Playwright headless runner with multi-locator fallback...");
    try {
      await runTestCase(token, id);
    } catch (err) {
      setRunningTest(false);
      setRunMessage("Failed to start regression test. Please ensure the backend is running.");
    }
  };

  const handleViewRunDetail = async (runId) => {
    setSelectedRunLoading(true);
    try {
      const res = await getRunDetail(token, runId);
      setSelectedRun(res.data);
    } catch (e) {
      alert("Failed to load run inspection details.");
    } finally {
      setSelectedRunLoading(false);
    }
  };

  return (
    <div className="layout-shell">
      {/* Modern Top Header */}
      <header className="app-header">
        <div className="brand" onClick={() => navigate("/dashboard")} style={{ cursor: "pointer" }}>
          <div className="brand-badge">
            <span className="brand-dot"></span>
          </div>
          <span className="brand-title">ChangeGuard AI</span>
          <span className="version-pill">v2.0 Regression Engine</span>
        </div>
        <div style={{ display: "flex", gap: 10 }}>
          <button className="btn btn-secondary" onClick={() => navigate("/dashboard")}>
            ← Back to Dashboard
          </button>
        </div>
      </header>

      <main className="page-container">
        {error && <div className="alert alert-danger">{error}</div>}

        {/* Hero Control Panel */}
        <section className="glass-card hero-section">
          <div className="hero-content">
            <div className="title-row">
              <span className="tag-pill">Test Case #{id}</span>
              <h1 className="page-title">Regression & Playback Inspector</h1>
            </div>
            <p className="page-subtitle">
              Inspect multi-locator fallback resilience and execute headless browser regression runs with cryptographic verification.
            </p>
          </div>

          <div className="hero-actions">
            <button
              className="btn btn-primary btn-glow"
              onClick={handleRunTest}
              disabled={runningTest || steps.length === 0}
            >
              {runningTest ? (
                <>
                  <span className="pulse-indicator"></span>
                  Executing Regression Run...
                </>
              ) : (
                <>
                  <span style={{ fontSize: 16 }}>▶</span>
                  Run Regression Test
                </>
              )}
            </button>
          </div>
        </section>

        {/* Live Execution Alert Banner */}
        {runMessage && (
          <div
            className={`alert ${
              runMessage.includes("failed") || runMessage.includes("Failed")
                ? "alert-danger"
                : runMessage.includes("passed")
                ? "alert-success"
                : "alert-info"
            }`}
            style={{ marginTop: 16 }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              {runningTest && <span className="pulse-dot"></span>}
              <span>{runMessage}</span>
            </div>
          </div>
        )}

        {/* Recorded Steps Card */}
        <section className="card" style={{ marginTop: 24 }}>
          <div className="card-header-row">
            <div>
              <h3 className="card-heading">Recorded Interaction Steps</h3>
              <p className="card-subheading">Candidate fallback locators captured during live recording session.</p>
            </div>
            <span className="count-pill">{steps.length} Steps</span>
          </div>

          {loading && <div className="skeleton-loader">Loading interaction steps...</div>}

          {!loading && steps.length === 0 && (
            <div className="empty-state">No recorded steps found for this test case.</div>
          )}

          {!loading && steps.length > 0 && (
            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th style={{ width: 60 }}>#</th>
                    <th>Action & Description</th>
                    <th style={{ width: 120 }}>Type</th>
                    <th>Input Value</th>
                    <th>Fallback Candidate Locators</th>
                  </tr>
                </thead>
                <tbody>
                  {steps.map((s) => (
                    <tr key={s.id}>
                      <td className="mono-order">{s.step_order}</td>
                      <td className="action-title">{s.description || "—"}</td>
                      <td>
                        <span className="badge badge-action">{s.action_type}</span>
                      </td>
                      <td className="mono-value">{s.input_value || "—"}</td>
                      <td>
                        <div className="locators-wrap">
                          {s.candidate_locators?.map((l, i) => (
                            <span key={i} className="locator-chip" title={`${l.strategy}: ${l.value}`}>
                              <span className="chip-strat">{l.strategy}</span>
                              <span className="chip-val">{l.value}</span>
                            </span>
                          ))}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        {/* Regression Run History Card */}
        <section className="card" style={{ marginTop: 24 }}>
          <div className="card-header-row">
            <div>
              <h3 className="card-heading">Regression Run History</h3>
              <p className="card-subheading">Historical execution logs, pass/fail status, and locator resolution benchmarks.</p>
            </div>
            <span className="count-pill">{runs.length} Runs</span>
          </div>

          {runs.length === 0 ? (
            <div className="empty-state">
              No regression runs recorded yet. Click <strong>"Run Regression Test"</strong> to trigger the headless runner.
            </div>
          ) : (
            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Run ID</th>
                    <th>Status</th>
                    <th>Steps Passed</th>
                    <th>Duration</th>
                    <th>Triggered By</th>
                    <th>Executed At</th>
                    <th style={{ textAlign: "right" }}>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {runs.map((r) => (
                    <tr key={r.id}>
                      <td className="mono-order">#{r.id}</td>
                      <td>
                        <span
                          className={`badge ${
                            r.status === "passed"
                              ? "badge-success"
                              : r.status === "running"
                              ? "badge-warning"
                              : "badge-danger"
                          }`}
                        >
                          {r.status === "running" && <span className="pulse-dot-small"></span>}
                          {r.status}
                        </span>
                      </td>
                      <td>
                        <span className="text-bold">{r.steps_passed}</span>
                        <span className="text-dim"> / {r.steps_total}</span>
                      </td>
                      <td className="mono-value">{r.duration_ms ? `${r.duration_ms}ms` : "—"}</td>
                      <td className="text-dim">{r.triggered_by || "tester"}</td>
                      <td className="text-dim" style={{ fontSize: 13 }}>
                        {r.started_at ? new Date(r.started_at).toLocaleString() : "—"}
                      </td>
                      <td style={{ textAlign: "right" }}>
                        <button
                          className="btn btn-secondary btn-sm"
                          onClick={() => handleViewRunDetail(r.id)}
                        >
                          Inspect Run
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
                <section className="card" style={{ marginTop: 24 }}>
          <div className="card-header-row">
            <div>
              <h3 className="card-heading">Change Intelligence Timeline</h3>
              <p className="card-subheading">Detected UI drift, self-healing events, and new failures compared to the previous run.</p>
            </div>
            <span className="count-pill">{changeEvents.length} Events</span>
          </div>

          {changeEvents.length === 0 ? (
            <div className="empty-state">
              No changes detected yet. Run this test case at least twice to start comparing runs.
            </div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {changeEvents.map((e) => (
                <div
                  key={e.id}
                  style={{
                    display: "flex",
                    alignItems: "flex-start",
                    gap: 12,
                    padding: "12px 14px",
                    borderRadius: 10,
                    background: "var(--bg-card)",
                    border: "1px solid var(--border-subtle)",
                  }}
                >
                  <span
                    className={`badge ${
                      e.severity === "high" ? "badge-danger" : e.severity === "medium" ? "badge-warning" : "badge-success"
                    }`}
                  >
                    {e.change_type.replace("_", " ")}
                  </span>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: 14, color: "var(--text-primary)" }}>{e.description}</div>
                    <div style={{ fontSize: 12, color: "var(--text-muted)", marginTop: 4 }}>
                      Run #{e.run_id} vs #{e.previous_run_id} · {new Date(e.detected_at).toLocaleString()}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
        {/* Modal: Run Inspection Breakdown */}
        {selectedRun && (
          <div className="modal-backdrop" onClick={() => setSelectedRun(null)}>
            <div className="modal-card" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <div>
                  <h3 className="modal-title">Run #{selectedRun.id} Execution Breakdown</h3>
                  <p className="modal-subtitle">Step-by-step resolution & timing</p>
                </div>
                <button className="close-btn" onClick={() => setSelectedRun(null)}>✕</button>
              </div>

              <div className="modal-metrics-bar">
                <div className="metric-pill">
                  <span className="metric-lbl">Status</span>
                  <span className={`badge ${selectedRun.status === "passed" ? "badge-success" : "badge-danger"}`}>
                    {selectedRun.status}
                  </span>
                </div>
                <div className="metric-pill">
                  <span className="metric-lbl">Duration</span>
                  <span className="metric-val">{selectedRun.duration_ms}ms</span>
                </div>
                <div className="metric-pill">
                  <span className="metric-lbl">Steps</span>
                  <span className="metric-val">{selectedRun.steps_passed} / {selectedRun.steps_total} passed</span>
                </div>
              </div>

              {selectedRun.error_message && (
                <div className="alert alert-danger" style={{ marginBottom: 16 }}>
                  <strong>Failure Root Cause:</strong> {selectedRun.error_message}
                </div>
              )}

              <div className="table-responsive">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th style={{ width: 50 }}>#</th>
                      <th>Action</th>
                      <th>Status</th>
                      <th>Resolved Locator Strategy</th>
                      <th style={{ textAlign: "right" }}>Time</th>
                    </tr>
                  </thead>
                  <tbody>
                    {selectedRun.steps?.map((st) => (
                      <tr key={st.id}>
                        <td className="mono-order">{st.step_order}</td>
                        <td className="action-title">{st.description || st.action_type}</td>
                        <td>
                          <span className={`badge ${st.status === "passed" ? "badge-success" : "badge-danger"}`}>
                            {st.status}
                          </span>
                        </td>
                        <td>
                          {st.resolved_locator_strategy ? (
                            <span className="locator-chip chip-resolved">
                              <span className="chip-strat">{st.resolved_locator_strategy}</span>
                              <span className="chip-val">{st.resolved_locator_value}</span>
                            </span>
                          ) : (
                            <span className="text-dim">—</span>
                          )}
                        </td>
                        <td className="mono-value" style={{ textAlign: "right" }}>{st.execution_time_ms}ms</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Floating Refresh Action Button */}
      <button className="fab" onClick={loadData} title="Refresh Page Data">
        <span style={{ fontSize: 18 }}>🔄</span>
      </button>
    </div>
  );
}