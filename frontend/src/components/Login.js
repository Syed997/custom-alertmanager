import React, { useState } from "react";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:5000";

const Login = ({ onLoginSuccess, onSwitchToSignup }) => {
  const [formData, setFormData] = useState({
    mail: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (res.ok) {
        // Store the access token
        localStorage.setItem("access_token", data["access token"]);
        alert("Login successful!");
        onLoginSuccess();
      } else {
        setError(data.unautorized || data.error || "Login failed");
      }
    } catch (error) {
      setError("Error: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="auth-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit} className="auth-form">
        <input
          type="email"
          name="mail"
          placeholder="Email"
          value={formData.mail}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        {error && <p className="error-message">{error}</p>}
        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>
      <p className="auth-switch">
        Don't have an account?{" "}
        <button onClick={onSwitchToSignup} className="link-button">
          Sign Up
        </button>
      </p>
    </div>
  );
};

export default Login;
