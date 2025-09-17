import { Button } from "@material-ui/core";
import TextField from "@material-ui/core/TextField";
import axios from "axios";
import React, { useState } from "react";
import "./ForgotPassword.css";

export default function ForgotPasswordPage() {
  const [emailValue, setEmailValue] = useState("");
  const [status, setStatus] = useState(null); // null: no status, 'success', 'error', 'invalid'

  const isValidEmail = (email) => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  };

  const handleSubmit = async () => {
    if (!isValidEmail(emailValue)) {
      setStatus("invalid");
      return;
    }

    try {
      await axios.post("/request_password_reset", {
        email: emailValue,
      });
      setStatus("success");
    } catch (error) {
      console.error(error);
      setStatus("error");
    }
  };

  return (
    <div className="forgot-password-container">
      <div className="card">
        <h1>Forgot your password?</h1>
        <h2>No problem, request a password reset to your email here.</h2>
        <TextField
          label="Email"
          variant="standard"
          className="email-input"
          type="email"
          value={emailValue}
          onChange={(e) => {
            setEmailValue(e.target.value);
            setStatus(null);
          }}
          error={status === "error" || status === "invalid"}
          helperText={
            status === "error"
              ? "No account was found with this email."
              : status === "success"
              ? "Email was sent successfully."
              : status === "invalid"
              ? "Please enter a valid email address."
              : ""
          }
        />
        <div className="btn-container">
          <Button
            variant="contained"
            className="btn"
            disabled={emailValue.trim() === ""}
            onClick={handleSubmit}
          >
            Send Email
          </Button>
        </div>
      </div>
    </div>
  );
}
