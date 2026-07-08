"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Stack, Typography, TextField, Button, Alert } from "@mui/material";
import { useSignUp } from "../hooks/use-sign-up";

export default function SignupForm() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const { signUpMutation, signUpError, isSignUpPending, isSignUpSuccess } = useSignUp();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    signUpMutation(
      { email, password, username },
      {
        onSuccess: () => {
          router.push("/projects");
        },
      }
    );
  };

  return (
    <Stack
      component="form"
      onSubmit={handleSubmit}
      spacing={2}
      sx={{ mt: 3, minWidth: "300px", textAlign: "center" }}
    >
      <Typography variant="h5" sx={{ fontWeight: "medium" }}>
        Sign Up
      </Typography>

      {signUpError && (
        <Alert severity="error">
          {(signUpError as Error).message || "Failed to sign up."}
        </Alert>
      )}

      {isSignUpSuccess && (
        <Alert severity="success">
          Signed up successfully! You can now sign in.
        </Alert>
      )}

      <TextField
        label="Username"
        type="text"
        autoComplete="username"
        variant="standard"
        fullWidth
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        disabled={isSignUpPending || isSignUpSuccess}
        required
      />
      <TextField
        label="Email"
        type="email"
        autoComplete="email"
        variant="standard"
        fullWidth
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        disabled={isSignUpPending || isSignUpSuccess}
        required
      />
      <TextField
        label="Password"
        type="password"
        autoComplete="new-password"
        variant="standard"
        fullWidth
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        disabled={isSignUpPending || isSignUpSuccess}
        required
      />
      <Button
        type="submit"
        variant="contained"
        fullWidth
        sx={{ mt: 1 }}
        disabled={isSignUpPending || isSignUpSuccess}
      >
        {isSignUpPending ? "Signing Up..." : "Sign Up"}
      </Button>
    </Stack>
  );
}
