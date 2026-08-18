import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getTestCases } from "../api";

export default function Dashboard() {
  const [testCases, setTestCases] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem("token");
  const navigate = useNavigate();

  const [recTargetUrl, setRecTargetUrl] = useState("https://www.wikipedia.org");
  const [recName, setRecName] = useState("");
  const [recMessage, setRecMessage] = useState("");
  const [recording, setRecording] = useState(false);
  const [recLog, setRecLog] = useState([]);

  const loadTestCases = () => {
    setLoading(true);
    getTestCases(token)
      .then((res) => setTestCases(res.data))
      .catch(() => setError("Failed to load test cases"))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadTestCases();
    // eslint-disable-next-line
  }, [token]);

  useEffect(() => {
    if (!recording) return;
    const interval = setInterval(async () => {
      try {
        const res = await fetch("http://127.0.0.1:5000/recording/status", {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await res.json();
        setRecLog(data.log || []);
        if (!data.running) {
          setRecording(false);
          if (data.error) {
            setRecMessage(`Error: ${data.error}`);
          } else {
            setRecMessage("Recording complete — test case saved below.");
            loadTestCases();
          }
        }
      } catch (e) {}
    }, 1500);
    return () => clearInterval(interval);
    // eslint-disable-next-line
  }, [recording]);

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const startRecording = async () => {
    if (!recTargetUrl || !recName) {
      setRecMessage("Please enter both a name and a target URL.");
      return;
    }
    setRecording(true);
    setRecLog([]);
    setRecMessage("");
    try {
      const res = await fetch("http://127.0.0.1:5000/recording/start", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ target_url: recTargetUrl, name: recName }),
      });
      if (!res.ok) {
        const data = await res.json();
        setRecMessage(`Error: ${data.error || "Could not start recording"}`);
        setRecording(false);
      }
    } catch (err) {
      setRecMessage("Failed to reach the server. Is the backend running?");
      setRecording(false);
    }
  };

  const uniqueSites = new Set(testCases.map((tc) => tc.target_url)).size;

  return (
    <div>
      <div className="app-header">
        <div className="brand">
          <span className="brand-dot"></span>
          ChangeGuard AI
        </div>
        <button className="btn btn-secondary" onClick={logout}>Logout</button>
      </div>

      <div className="page-container">
        <div className="hero-banner">
          <h1>🎬 Smart Test Recording Studio</h1>
          <p>
            Record real user actions on any live website — no scripting required.
            Every action is captured, timestamped, and permanently logged in a
            tamper-evident audit trail.
          </p>
        </div>

        <div className="stats-row">
          <div className="stat-card">
            <div className="stat-value">{testCases.length}</div>
            <div className="stat-label">Total Test Cases</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{uniqueSites}</div>
            <div className="stat-label">Websites Tested</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{recording ? "●" : "—"}</div>
            <div className="stat-label">{recording ? "Recording Live" : "Idle"}</div>
          </div>
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        <div className="card">
          <h3>🌐 Record a New Test Case</h3>
          <div style={{ display: "flex", gap: 12, alignItems: "flex-end", flexWrap: "wrap" }}>
            <div style={{ flex: 1, minWidth: 180 }}>
              <label className="field-label">Test case name</label>
              <input
                className="input"
                value={recName}
                onChange={(e) => setRecName(e.target.value)}
                placeholder="e.g. Wikipedia Search Test"
                disabled={recording}
              />
            </div>
            <div style={{ flex: 2, minWidth: 240 }}>
              <label className="field-label">Target website URL</label>
              <input
                className="input"
                value={recTargetUrl}
                onChange={(e) => setRecTargetUrl(e.target.value)}
                placeholder="https://your-real-website.com"
                disabled={recording}
              />
            </div>
            <button className="btn btn-primary" onClick={startRecording} disabled={recording}>
              {recording ? "Recording..." : "🔴 Start Recording"}
            </button>
          </div>

          {recording && (
            <div className="alert alert-info" style={{ marginTop: 14 }}>
              <span className="pulse-dot"></span>
              Browser is open — interact with the site now (up to 60 seconds).
            </div>
          )}

          {recMessage && !recording && (
            <div className={`alert ${recMessage.startsWith("Error") ? "alert-danger" : "alert-success"}`} style={{ marginTop: 14 }}>
              {recMessage}
            </div>
          )}

          {recLog.length > 0 && (
            <div className="log-box">
              {recLog.map((line, i) => (
                <div key={i} className="log-line">$ {line}</div>
              ))}
            </div>
          )}
        </div>

        <div className="card">
          <h3>📋 Recorded Test Cases</h3>
          {loading && <p style={{ color: "var(--color-text-secondary)" }}>Loading...</p>}

          {!loading && testCases.length === 0 && (
            <div className="empty-state">No test cases recorded yet. Start one above.</div>
          )}

          {!loading && testCases.length > 0 && (
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Target URL</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {testCases.map((tc) => (
                  <tr key={tc.id} onClick={() => navigate(`/testcase/${tc.id}`)}>
                    <td>#{tc.id}</td>
                    <td>{tc.name}</td>
                    <td style={{ color: "var(--color-text-secondary)" }}>{tc.target_url}</td>
                    <td><span className="badge badge-active">{tc.status}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      <button className="fab" onClick={loadTestCases} title="Refresh test cases">
        🔄
      </button>
    </div>
  );
}