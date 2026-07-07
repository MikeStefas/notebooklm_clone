"use client";

import React, { useState } from "react";
import { Stack, Typography, TextField, Button, Alert } from "@mui/material";
import { useSignIn } from "../hooks/use-sign-in";
import { getAccessToken, getRefreshToken } from "@/app/shared/cookies";

export default function SigninForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const { mutate, isPending, error, isSuccess } = useSignIn();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutate(
      { email, password },
      {
        onSuccess: async () => {
          const access = await getAccessToken();
          const refresh = await getRefreshToken();
          console.log("Access Token from cookies:", access);
          console.log("Refresh Token from cookies:", refresh);
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

      {error && (
        <Alert severity="error">
          {(error as Error).message || "Invalid email or password."}
        </Alert>
      )}

      {isSuccess && (
        <Alert severity="success">
          Signed in successfully! Check browser console for cookies.
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
        disabled={isPending || isSuccess}
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
        disabled={isPending || isSuccess}
        required
      />
      <Button
        type="submit"
        variant="contained"
        fullWidth
        sx={{ mt: 1 }}
        disabled={isPending || isSuccess}
      >
        {isPending ? "Signing In..." : "Sign In"}
      </Button>
    </Stack>
  );
}
