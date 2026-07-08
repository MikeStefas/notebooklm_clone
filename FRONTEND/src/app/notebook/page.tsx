"use client";

import { Box, Stack } from "@mui/material";

export default function NotebookPage() {
  return (
    <Stack direction={"row"} sx={{ height: "100vh" }}>
      <Box sx={{ width: "20%", backgroundColor: "red", minWidth: "300px" }}>
        a
      </Box>
      <Box sx={{ width: "70%", backgroundColor: "blue" }}>b</Box>
      <Box sx={{ width: "10%", backgroundColor: "green" }}>c</Box>
    </Stack>
  );
}
