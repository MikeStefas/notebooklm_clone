"use client";

import { useState } from "react";
import { Stack, Typography, Button, CircularProgress } from "@mui/material";
import { useSearchParams, useRouter } from "next/navigation";
import { useGetProjectById } from "@/features/projects/hooks/use-get-project-by-id";
import NotebookSidebar from "@/features/notebook/components/NotebookSidebar";
import ChatArea from "@/features/notebook/components/ChatArea";
import DocumentViewer from "@/features/files/components/DocumentViewer";
import { Box } from "@mui/material";

interface Message {
  id: string;
  sender: "user" | "assistant";
  text: string;
  timestamp: Date;
}

export default function NotebookPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const projectId = searchParams.get("projectId");

  const { project, isLoading, isError, error } = useGetProjectById(projectId!);
  const [selectedFileId, setSelectedFileId] = useState<string | null>(null);

  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      sender: "assistant",
      text: "Hi, ask me anything about your project documents.",
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState("");

  const handleSendMessage = () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      sender: "user",
      text: inputValue,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");

    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: "assistant",
          text: `Mock response: I got your query "${userMessage.text}". Full LLM integration is in progress.`,
          timestamp: new Date(),
        },
      ]);
    }, 1000);
  };

  if (isLoading) {
    return (
      <Stack sx={{ gap: 2, alignItems: "center", p: 4 }}>
        <CircularProgress />
        <Typography>Loading project details...</Typography>
      </Stack>
    );
  }

  if (isError) {
    return (
      <Stack sx={{ gap: 2, p: 4 }}>
        <Typography>
          Failed to load project: {(error as Error).message}
        </Typography>
        <Button variant="contained" onClick={() => router.push("/projects")}>
          Back to Projects
        </Button>
      </Stack>
    );
  }

  if (!project) {
    return (
      <Stack sx={{ gap: 2, p: 4 }}>
        <Typography>No project found</Typography>
        <Button variant="contained" onClick={() => router.push("/projects")}>
          Back to Projects
        </Button>
      </Stack>
    );
  }

  return (
    <Stack sx={{ flexDirection: "row", height: "100vh", overflow: "hidden" }}>
      <NotebookSidebar
        project={project}
        projectId={projectId!}
        selectedFileId={selectedFileId}
        onSelectFile={setSelectedFileId}
      />
      <Box
        sx={{
          flexGrow: 1,
          display: "flex",
          flexDirection: "row",
          minWidth: 0,
          height: "100%",
        }}
      >
        <Box
          sx={{
            width: selectedFileId ? "50%" : "100%",
            transition: "width 0.3s ease",
            height: "100%",
          }}
        >
          <ChatArea
            messages={messages}
            inputValue={inputValue}
            setInputValue={setInputValue}
            handleSendMessage={handleSendMessage}
          />
        </Box>

        {selectedFileId && (
          <DocumentViewer
            projectId={projectId!}
            fileId={selectedFileId}
            fileName={
              project.files?.find((f) => f.id === selectedFileId)?.name ||
              "Document"
            }
            onClose={() => setSelectedFileId(null)}
          />
        )}
      </Box>
    </Stack>
  );
}
