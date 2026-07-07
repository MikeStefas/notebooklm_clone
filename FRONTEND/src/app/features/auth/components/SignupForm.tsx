"use client";

import React, { useState } from "react";
import { Stack, Typography, TextField, Button, Alert } from "@mui/material";

export default function SignupForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <Stack
      component="form"
      spacing={2}
      sx={{ mt: 3, minWidth: "300px", textAlign: "center" }}
    >
      <Typography variant="h5" sx={{ fontWeight: "medium" }}>
        Sign Up
      </Typography>
      <TextField
        label="Email"
        type="email"
        autoComplete="email"
        variant="standard"
        fullWidth
        value={email}
        onChange={(e) => setEmail(e.target.value)}
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
        required
      />
      <Button type="submit" variant="contained" fullWidth sx={{ mt: 1 }}>
        Sign Up
      </Button>
    </Stack>
  );
}
