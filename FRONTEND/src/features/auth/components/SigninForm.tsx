"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Stack, Typography, TextField, Button, Alert } from "@mui/material";
import { useSignIn } from "../hooks/use-sign-in";

export default function SigninForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const { signInMutation, signInError, isSignInPending } = useSignIn();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    signInMutation(
      { email, password },
      {
        onSuccess: async () => {
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
        Sign In
      </Typography>

      {signInError && (
        <Alert severity="error">
          {(signInError as Error).message || "Invalid email or password."}
        </Alert>
      )}

      <TextField
        label="Email"
        type="email"
        autoComplete="email"
        variant="standard"
        fullWidth
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        disabled={isSignInPending}
        required
      />
      <TextField
        label="Password"
        type="password"
        autoComplete="current-password"
        variant="standard"
        fullWidth
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        disabled={isSignInPending}
        required
      />
      <Button
        type="submit"
        variant="contained"
        fullWidth
        sx={{ mt: 1 }}
        disabled={isSignInPending}
      >
        {isSignInPending ? "Signing In..." : "Sign In"}
      </Button>
    </Stack>
  );
}
