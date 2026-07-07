"use client";
import { Box, Button, Stack, Typography } from "@mui/material";
import { useState } from "react";
import SignupForm from "./features/auth/components/SignupForm";
import SigninForm from "./features/auth/components/SigninForm";

export default function Home() {
  const [showForm, setShowForm] = useState("none");
  return (
    <Stack
      sx={{
        alignItems: "center",
        justifyContent: "center",
        flexGrow: 1,
        minHeight: "75vh",
        mx: "auto",
        px: 2,
      }}
      spacing={4}
    >
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography
          variant="h3"
          sx={{ textAlign: "center", fontWeight: "bold" }}
        >
          SourceLM
        </Typography>
        <Typography variant="h5" sx={{ textAlign: "center", mt: 1 }}>
          Transform your documents into a private AI-powered knowledge base.
        </Typography>
      </Box>
      <Box
        sx={{ display: "flex", flexDirection: "column", alignItems: "center" }}
      >
        <Stack
          direction="row"
          spacing={2}
          sx={{ alignItems: "center", justifyContent: "center" }}
        >
          <Button onClick={() => setShowForm("signup")} variant="contained">
            Get Started
          </Button>
          <Button onClick={() => setShowForm("signin")} variant="outlined">
            Sign In
          </Button>
        </Stack>
        {showForm === "signup" && <SignupForm />}
        {showForm === "signin" && <SigninForm />}
      </Box>
    </Stack>
  );
}
