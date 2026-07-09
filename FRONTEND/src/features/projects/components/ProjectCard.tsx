import { Box, Typography } from "@mui/material";
import { useRouter } from "next/navigation";
import { Project } from "../types";

export const ProjectCard = ({ project }: { project: Project }) => {
  const router = useRouter();

  return (
    <Box
      onClick={() => router.push(`/notebook?projectId=${project.id}`)}
      sx={{
        border: "1px solid #ccc",
        borderRadius: "8px",
        p: 2,
        height: "100px",
        cursor: "pointer",
        "&:hover": {
          bgcolor: "rgba(255, 255, 255, 0.05)",
        },
      }}
    >
      <Typography variant="h6">{project.title}</Typography>
    </Box>
  );
};
