import SessionProvider from "@/shared/session-provider";
import { Box } from "@mui/material";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <SessionProvider>
      <Box
        sx={{
          p: 2,
          display: "flex",
          flexDirection: "column",
          height: "100vh",
        }}
      >
        {children}
      </Box>
    </SessionProvider>
  );
}
