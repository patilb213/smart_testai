import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getStepsForTestCase } from "../api";

export default function TestCaseDetail() {
  const { id } = useParams();
  const [steps, setSteps] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem("token");
  const navigate = useNavigate();

  useEffect(() => {
    setLoading(true);
    getStepsForTestCase(token, id)
      .then((res) => setSteps(res.data))
      .catch(() => setError("Failed to load steps"))
      .finally(() => setLoading(false));
  }, [token, id]);

  return (
    <div>
      <div className="app-header">
        <div className="brand">
          <span className="brand-dot"></span>
          ChangeGuard AI
        </div>
        <button className="btn btn-secondary" onClick={() => navigate("/dashboard")}>Back to Dashboard</button>
      </div>

      <div className="page-container">
        <div className="card">
          <h3>Test Case #{id} — Recorded Steps</h3>
          {error && <div className="alert alert-danger">{error}</div>}
          {loading && <p style={{ color: "var(--color-text-secondary)" }}>Loading...</p>}

          {!loading && steps.length === 0 && !error && (
            <div className="empty-state">No steps found for this test case.</div>
          )}

          {!loading && steps.length > 0 && (
            <table className="data-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Action</th>
                  <th>Locators</th>
                  <th>Value</th>
                  <th>Page</th>
                </tr>
              </thead>
              <tbody>
                {steps.map((s) => (
                  <tr key={s.id} style={{ cursor: "default" }}>
                    <td>{s.step_order}</td>
                    <td><span className="badge badge-active">{s.action_type}</span></td>
                    <td>
                      {s.candidate_locators?.map((l, i) => (
                        <span key={i} className="locator-chip">{l.strategy}: {l.value}</span>
                      ))}
                    </td>
                    <td>{s.input_value || "—"}</td>
                    <td style={{ fontSize: 12, color: "var(--color-text-secondary)", wordBreak: "break-all" }}>
                      {s.page_url}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}