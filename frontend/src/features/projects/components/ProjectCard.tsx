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
        cursor: "pointer",
        transition: "all 0.2s ease-in-out",
        "&:hover": {
          bgcolor: "action.hover",
          borderColor: "primary.main",
        },
      }}
    >
      <Typography variant="h6" sx={{ fontWeight: "bold" }}>
        {project.title}
      </Typography>

      {project.file ? (
        <Box sx={{ mt: 1, display: "flex", alignItems: "center", gap: 1 }}>
          <Typography
            variant="body2"
            color="text.secondary"
            noWrap
            sx={{ maxWidth: "200px" }}
          >
            File: {project.file.name}
          </Typography>
        </Box>
      ) : (
        <Typography
          variant="caption"
          color="text.secondary"
          sx={{ mt: 1, display: "block" }}
        >
          No file attached
        </Typography>
      )}
    </Box>
  );
};
