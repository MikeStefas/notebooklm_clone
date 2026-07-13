import {
  Box,
  Stack,
  Typography,
  Button,
  CircularProgress,
} from "@mui/material";
import { useViewFile } from "@/features/files/hooks/use-view-file";

interface DocumentViewerProps {
  projectId: string;
  fileId: string;
  fileName: string;
  onClose: () => void;
}

export default function DocumentViewer({
  projectId,
  fileId,
  fileName,
  onClose,
}: DocumentViewerProps) {
  const { url: fileUrl, isPending: isLoadingFile } = useViewFile(
    projectId,
    fileId
  );

  return (
    <Box
      sx={{
        width: "50%",
        height: "100%",
        borderLeft: "1px solid rgba(0, 0, 0, 0.12)",
        display: "flex",
        flexDirection: "column",
        bgcolor: "background.paper",
      }}
    >
      <Stack
        direction="row"
        sx={{
          p: 2,
          borderBottom: "1px solid rgba(0, 0, 0, 0.12)",
          bgcolor: "action.hover",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Typography variant="subtitle1" sx={{ maxWidth: "75%" }}>
          {fileName}
        </Typography>
        <Button size="small" onClick={onClose}>
          Close
        </Button>
      </Stack>

      <Box sx={{ flexGrow: 1, position: "relative", minHeight: 0 }}>
        {isLoadingFile ? (
          <Stack
            sx={{
              height: "100%",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <CircularProgress />
            <Typography sx={{ mt: 2 }}>Loading document...</Typography>
          </Stack>
        ) : fileUrl ? (
          <iframe
            src={fileUrl}
            width="100%"
            height="100%"
            style={{ border: "none" }}
            title="Document Viewer"
          />
        ) : (
          <Stack
            sx={{
              height: "100%",
              justifyContent: "center",
              alignItems: "center",
              p: 2,
            }}
          >
            <Typography color="error">
              Failed to generate document view URL.
            </Typography>
          </Stack>
        )}
      </Box>
    </Box>
  );
}
