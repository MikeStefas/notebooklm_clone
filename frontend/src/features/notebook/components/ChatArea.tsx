import { Box, Stack, Typography, TextField, Button } from "@mui/material";
import { usePostMessage } from "../hooks/use-post-message";

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
  const { postMessage, isPostMessagePending } = usePostMessage(projectId);

  const handleSendMessage = () => {
    if (!inputValue.trim() || isPostMessagePending) return;

    postMessage(inputValue, {
      onSuccess: (data) => {
        console.log(data);
      },
      onError: (err) => {
        console.error("Embedding search failed:", err);
      },
    });

    setInputValue("");
  };

  return (
    <Stack sx={{ gap: 2, p: 2, width: "100%", height: "100%", minHeight: 0 }}>
      <Box
        sx={{
          flexGrow: 1,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          p: 4,
          textAlign: "center",
        }}
      ></Box>

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
