import SessionProvider from "@/shared/session-provider";
import { Box } from "@mui/material";

export default function NotebookLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <SessionProvider>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          minHeight: "100vh",
        }}
      >
        {children}
      </Box>
    </SessionProvider>
  );
}
