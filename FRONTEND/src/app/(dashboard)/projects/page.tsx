"use client";

import { useGetName } from "@/features/auth/hooks";
import { Box, Stack, Typography } from "@mui/material";

export default function ProjectsPage() {
  const username = useGetName();

  return (
    <Stack sx={{ flex: 1 }}>
      <Stack
        spacing={2}
        direction="column"
        sx={{
          flex: 1,
          alignItems: "center",
          width: "100%",
          maxHeight: "80%",
          m: "auto",
        }}
      >
        <Typography variant="h4" sx={{ fontWeight: "bold" }}>
          Welcome, {username}.
        </Typography>
        <Typography variant="h5">Your Projects:</Typography>
        <Box
          sx={{
            bgcolor: "#16213e",
            width: "60%",
            height: "100%",
            display: "grid",
          }}
        ></Box>
      </Stack>
    </Stack>
  );
}
