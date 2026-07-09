import { useState } from "react";
import { Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField } from "@mui/material";
import { useCreateProject } from "@/features/projects/hooks/use-create-project";

export function CreateProjectButton() {
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState("");
  const { createProject, isPending } = useCreateProject();

  const handleCreate = () => {
    if (!title.trim()) return;
    createProject(title, {
      onSuccess: () => {
        alert("success");
        setTitle("");
        setOpen(false);
      },
      onError: (err) => {
        alert("Failed to create project: " + err.message);
      },
    });
  };

  return (
    <>
      <Button variant="contained" onClick={() => setOpen(true)}>
        Create Project
      </Button>

      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>Create New Project</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Project Title"
            type="text"
            fullWidth
            variant="standard"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button onClick={handleCreate} disabled={isPending || !title.trim()}>
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
