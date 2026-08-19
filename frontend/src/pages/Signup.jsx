import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { signup } from "../api";

export default function Signup() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await signup(name, email, password);
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.error || "Signup failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-shell">
      <div className="login-panel">
        <div className="brand" style={{ marginBottom: 20 }}>
          <div className="brand-badge"><span className="brand-dot"></span></div>
          <span className="brand-title">ChangeGuard AI</span>
        </div>
        <div className="login-title">Create Account</div>
        <div className="login-subtitle">Join ChangeGuard AI</div>

        <form onSubmit={handleSubmit}>
          <div className="field-group">
            <label className="field-label">Full Name</label>
            <input className="input" value={name} onChange={(e) => setName(e.target.value)} placeholder="Your name" required />
          </div>
          <div className="field-group">
            <label className="field-label">Email</label>
            <input type="email" className="input" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@company.com" required />
          </div>
          <div className="field-group">
            <label className="field-label">Password</label>
            <input type="password" className="input" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" required />
          </div>

          {error && <div className="alert alert-danger" style={{ marginBottom: 16 }}>{error}</div>}

          <button type="submit" className="btn btn-primary btn-glow" style={{ width: "100%" }} disabled={loading}>
            {loading ? "Creating account..." : "Sign Up"}
          </button>
        </form>

        <p style={{ textAlign: "center", marginTop: 20, fontSize: 13, color: "var(--text-secondary)" }}>
          Already have an account? <Link to="/login" className="link-accent">Sign in</Link>
        </p>
      </div>
    </div>
  );
}