"use client";

import { useGetName } from "@/features/auth/hooks/use-get-name";
import { Stack, Typography } from "@mui/material";
import { useGetProjects } from "@/features/projects/hooks/use-get-projects";
import { ProjectList } from "@/features/projects/components/ProjectList";

export default function ProjectsPage() {
  const username = useGetName();
  const { data: projects, error, isLoading, isError } = useGetProjects();

  return (
    <Stack sx={{ p: 4, alignItems: "center" }}>
      <Stack
        spacing={2}
        sx={{ width: "100%", maxWidth: "60%", alignItems: "center" }}
      >
        <Typography variant="h4" sx={{ fontWeight: "bold" }}>
          Welcome, {username || "User"}.
        </Typography>
        <Typography variant="h5">Your Projects:</Typography>

        {isLoading && <Typography>Loading projects...</Typography>}
        {isError && (
          <Typography color="error">
            Failed to load projects: {(error as Error).message}
          </Typography>
        )}

        {projects && <ProjectList projects={projects} />}
      </Stack>
    </Stack>
  );
}
