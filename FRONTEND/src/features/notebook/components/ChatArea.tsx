import { Box, Stack, Typography, TextField, Button } from "@mui/material";

interface Message {
  id: string;
  sender: "user" | "assistant";
  text: string;
  timestamp: Date;
}

interface ChatAreaProps {
  messages: Message[];
  inputValue: string;
  setInputValue: (val: string) => void;
  handleSendMessage: () => void;
}

export default function ChatArea({
  messages,
  inputValue,
  setInputValue,
  handleSendMessage,
}: ChatAreaProps) {
  return (
    <Stack sx={{ gap: 2, p: 2, width: "100%", height: "100%", minHeight: 0 }}>
      <Box sx={{ flexGrow: 1, overflowY: "auto" }}>
        {messages.map((message) => (
          <Box
            key={message.id}
            sx={{
              my: 2,
              textAlign: message.sender === "user" ? "right" : "left",
            }}
          >
            <Typography variant="body1">{message.text}</Typography>
          </Box>
        ))}
      </Box>

      <Stack sx={{ flexDirection: "row", gap: 2, alignItems: "center" }}>
        <TextField
          fullWidth
          placeholder="Ask a question about your documents..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSendMessage();
            }
          }}
        />
        <Button
          variant="contained"
          onClick={handleSendMessage}
          disabled={!inputValue.trim()}
        >
          Send
        </Button>
      </Stack>
    </Stack>
  );
}
