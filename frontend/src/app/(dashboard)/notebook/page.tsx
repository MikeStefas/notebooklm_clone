"use client";

import { useState } from "react";
import { Stack, Typography, Button, CircularProgress } from "@mui/material";
import { useSearchParams, useRouter } from "next/navigation";
import { useGetProjectById } from "@/features/projects/hooks/use-get-project-by-id";
import NotebookSidebar from "@/features/files/components/NotebookSidebar";
import ChatArea from "@/features/messages/components/ChatArea";
import DocumentViewer from "@/features/files/components/DocumentViewer";
import { Box } from "@mui/material";

export default function NotebookPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const projectId = searchParams.get("projectId");

  const { project, isLoading, isError, error } = useGetProjectById(projectId!);
  const [selectedFileId, setSelectedFileId] = useState<string | null>(null);
  const [inputValue, setInputValue] = useState("");

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
            projectId={projectId!}
            inputValue={inputValue}
            setInputValue={setInputValue}
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
