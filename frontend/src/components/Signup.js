import React, { useState, useEffect } from "react";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:5000";

const Signup = ({ onSignupSuccess, onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    mail: "",
    password: "",
    confirmPassword: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // OTP States
  const [showOtpScreen, setShowOtpScreen] = useState(false);
  const [otp, setOtp] = useState("");
  const [otpLoading, setOtpLoading] = useState(false);
  const [otpError, setOtpError] = useState("");
  const [countdown, setCountdown] = useState(300); // 5 minutes = 300 seconds
  const [canResend, setCanResend] = useState(false);

  // Countdown timer
  useEffect(() => {
    let timer;
    if (showOtpScreen && countdown > 0) {
      timer = setTimeout(() => {
        setCountdown(countdown - 1);
      }, 1000);
    } else if (countdown === 0) {
      setCanResend(true);
    }
    return () => clearTimeout(timer);
  }, [countdown, showOtpScreen]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };
  // TODO: need to add domain check for email 
  // TODO: auto login after signup
  const handleSignup = async (e) => {
    e.preventDefault();
    setError("");

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/auth/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          mail: formData.mail,
          password: formData.password,
        }),
      });

      const data = await res.json();

      if (res.ok) {
        // Show OTP screen instead of calling onSignupSuccess
        setShowOtpScreen(true);
        setCountdown(300);
        setCanResend(false);
        setOtp("");
        setOtpError("");
      } else {
        setError(data.error || "Signup failed");
      }
    } catch (error) {
      setError("Network error: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleOtpSubmit = async (e) => {
    e.preventDefault();
    if (otp.length !== 6) {
      setOtpError("Please enter a 6-digit OTP");
      return;
    }

    setOtpLoading(true);
    setOtpError("");

    try {
      const res = await fetch(`${API_BASE}/auth/signup/verify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          mail: formData.mail,
          otp: otp,
          password: formData.password, // CRITICAL: Send password here!
        }),
      });

      const data = await res.json();

      if (res.ok) {
        alert("Account verified successfully! You can now log in.");
        onSignupSuccess();
      } else {
        setOtpError(data.error || "Invalid or expired OTP");
      }
    } catch (error) {
      setOtpError("Verification failed: " + error.message);
    } finally {
      setOtpLoading(false);
    }
  };

  const handleResendOtp = async () => {
    setOtpLoading(true);
    try {
      const res = await fetch(`${API_BASE}/auth/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          mail: formData.mail,
          password: formData.password,
        }),
      });

      if (res.ok) {
        setCountdown(300);
        setCanResend(false);
        setOtp("");
        setOtpError("");
        alert("New OTP sent to your email!");
      }
    } catch (error) {
      setOtpError("Failed to resend OTP");
    } finally {
      setOtpLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // If OTP screen is active, show OTP verification
  if (showOtpScreen) {
    return (
      <div className="auth-container">
        <h2>Verify Your Email</h2>
        <p>
          We sent a 6-digit code to <strong>{formData.mail}</strong>
        </p>

        <form onSubmit={handleOtpSubmit} className="auth-form">
          <input
            type="text"
            placeholder="Enter 6-digit OTP"
            value={otp}
            onChange={(e) => {
              if (/^\d*$/.test(e.target.value) && e.target.value.length <= 6) {
                setOtp(e.target.value);
              }
            }}
            maxLength="6"
            required
            autoFocus
            style={{
              textAlign: "center",
              letterSpacing: "8px",
              fontSize: "1.5rem",
            }}
          />

          {otpError && <p className="error-message">{otpError}</p>}

          <div style={{ margin: "20px 0", textAlign: "center" }}>
            <p>
              Time remaining: <strong>{formatTime(countdown)}</strong>
            </p>
            <button
              type="button"
              onClick={handleResendOtp}
              disabled={otpLoading || !canResend}
              className="link-button"
              style={{ opacity: canResend ? 1 : 0.5 }}
            >
              {otpLoading ? "Sending..." : "Resend OTP"}
            </button>
          </div>

          <button type="submit" disabled={otpLoading || otp.length !== 6}>
            {otpLoading ? "Verifying..." : "Verify & Complete Signup"}
          </button>
        </form>

        <p className="auth-switch">
          <button
            onClick={() => setShowOtpScreen(false)}
            className="link-button"
          >
            ← Back to Signup
          </button>
        </p>
      </div>
    );
  }

  // Default Signup Form
  return (
    <div className="auth-container">
      <h2>Sign Up</h2>
      <form onSubmit={handleSignup} className="auth-form">
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
          minLength="6"
        />
        <input
          type="password"
          name="confirmPassword"
          placeholder="Confirm Password"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
        />
        {error && <p className="error-message">{error}</p>}
        <button type="submit" disabled={loading}>
          {loading ? "Creating account..." : "Sign Up"}
        </button>
      </form>
      <p className="auth-switch">
        Already have an account?{" "}
        <button onClick={onSwitchToLogin} className="link-button">
          Login
        </button>
      </p>
    </div>
  );
};

export default Signup;
