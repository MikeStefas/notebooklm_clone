import {
  Box,
  Stack,
  Typography,
  TextField,
  Button,
  CircularProgress,
} from "@mui/material";
import { useHandleSendMessage } from "../hooks/use-pos";

interface ChatAreaProps {
  projectId: string;
  inputValue: string;
  setInputValue: (val: string) => void;
}

export default function ChatArea({
  inputValue,
  projectId,
  setInputValue,
}: ChatAreaProps) {
  const {
    handleSendMessage,
    displayedMessages,
    isGetAllMessagesLoading,
    isGetAllMessagesError,
    getAllMessagesError,
    isPostMessagePending,
  } = useHandleSendMessage({ projectId, inputValue, setInputValue });

  return (
    <Stack sx={{ gap: 2, p: 2, width: "100%", height: "100%", minHeight: 0 }}>
      <Box
        sx={{
          flexGrow: 1,
          overflowY: "auto",
          p: 2,
          display: "flex",
          flexDirection: "column",
          gap: 2,
        }}
      >
        {isGetAllMessagesLoading && (
          <Box sx={{ display: "flex", justifyContent: "center", mt: 4 }}>
            <CircularProgress size={24} />
          </Box>
        )}
        {isGetAllMessagesError && (
          <Typography color="error">
            Error: {getAllMessagesError?.message}
          </Typography>
        )}

        {displayedMessages.map((msg) => (
          <Box key={msg.id}>
            <Typography variant="body1">{msg.content}</Typography>
          </Box>
        ))}
      </Box>

      <Stack sx={{ flexDirection: "row", gap: 2, alignItems: "center" }}>
        <TextField
          fullWidth
          placeholder="Ask a question to search embeddings..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSendMessage();
            }
          }}
          disabled={isPostMessagePending}
        />
        <Button
          variant="contained"
          onClick={handleSendMessage}
          disabled={!inputValue.trim() || isPostMessagePending}
        >
          {isPostMessagePending ? "Searching..." : "Search"}
        </Button>
      </Stack>
    </Stack>
  );
}
