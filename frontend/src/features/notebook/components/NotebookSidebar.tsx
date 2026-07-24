import { Box, Typography, Button } from "@mui/material";
import { useRouter } from "next/navigation";
import { Project } from "@/features/projects/types";
import FileManager from "@/features/files/components/FileManager";

interface NotebookSidebarProps {
  project: Project;
  projectId: string;
  selectedFileId: string | null;
  onSelectFile: (fileId: string | null) => void;
}

export default function NotebookSidebar({
  project,
  projectId,
  selectedFileId,
  onSelectFile,
}: NotebookSidebarProps) {
  const router = useRouter();

  return (
    <Box
      sx={{
        p: 2,
        width: "15%",
        borderRight: 1,
        height: "100%",
        display: "flex",
        flexDirection: "column",
        minHeight: 0,
      }}
    >
      <Button onClick={() => router.push("/projects")}>Back</Button>
      <Typography variant="h4" sx={{ mt: 1 }}>
        {project.title}
      </Typography>

      <FileManager
        projectId={projectId}
        file={project.file}
        selectedFileId={selectedFileId}
        onSelectFile={onSelectFile}
      />
    </Box>
  );
}
