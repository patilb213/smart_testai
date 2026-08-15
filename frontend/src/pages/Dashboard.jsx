import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getTestCases } from "../api";
export default function Dashboard() {
  const [testCases, setTestCases] = useState([]);
  const [error, setError] = useState("");
  const token = localStorage.getItem("token");
  const navigate = useNavigate();
  useEffect(() => {
    getTestCases(token)
      .then((res) => setTestCases(res.data))
      .catch(() => setError("Failed to load test cases"));
  }, [token]);
  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };
  return (
    <div style={{ maxWidth: 800, margin: "40px auto", fontFamily: "sans-serif" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h2>ChangeGuard AI — Dashboard</h2>
        <button onClick={logout}>Logout</button>
      </div>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <table style={{ width: "100%", borderCollapse: "collapse", marginTop: 20 }}>
        <thead>
          <tr style={{ borderBottom: "2px solid #333", textAlign: "left" }}>
            <th style={{ padding: 8 }}>ID</th>
            <th style={{ padding: 8 }}>Name</th>
            <th style={{ padding: 8 }}>Target URL</th>
            <th style={{ padding: 8 }}>Status</th>
          </tr>
        </thead>
        <tbody>
          {testCases.map((tc) => (
            <tr key={tc.id} style={{ borderBottom: "1px solid #ddd" }}>
              <td style={{ padding: 8 }}>{tc.id}</td>
              <td style={{ padding: 8 }}>{tc.name}</td>
              <td style={{ padding: 8 }}>{tc.target_url}</td>
              <td style={{ padding: 8 }}>{tc.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}