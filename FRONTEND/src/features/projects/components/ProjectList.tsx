import { useState } from "react";
import { Grid, Stack, Button } from "@mui/material";
import { ProjectCard } from "./ProjectCard";
import { Project } from "../types";

interface ProjectListProps {
  projects: Project[];
}

export const ProjectList = ({ projects }: ProjectListProps) => {
  const [projectStart, setProjectStart] = useState(0);
  const projectEnd = projectStart + 12;

  const shown_projects = projects.slice(projectStart, projectEnd);

  function handleNextPage() {
    setProjectStart((prev) => prev + 12);
  }

  function handlePrevPage() {
    setProjectStart((prev) => prev - 12);
  }

  return (
    <Stack sx={{ width: "100%", alignItems: "center" }}>
      <Grid
        container
        spacing={2}
        sx={{
          p: 1,
          mt: 1,
          width: "100%",
          height: "60vh",
          overflowY: "auto",
          alignContent: "flex-start",
        }}
      >
        {shown_projects.map((project) => (
          <Grid key={project.id} size={{ xs: 12, sm: 6, md: 4 }}>
            <ProjectCard project={project} />
          </Grid>
        ))}
      </Grid>
      <Stack
        direction="row"
        sx={{
          justifyContent: "space-between",
          width: "70%",
          mx: "auto",
          mt: 2,
        }}
      >
        <Button onClick={handlePrevPage} disabled={projectStart <= 0}>
          Prev
        </Button>
        <Button
          onClick={handleNextPage}
          disabled={projectEnd >= projects.length}
        >
          Next
        </Button>
      </Stack>
    </Stack>
  );
};
