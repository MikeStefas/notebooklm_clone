import { useState } from "react";
import { Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Box, Typography, CircularProgress } from "@mui/material";
import { useCreateProject } from "@/features/projects/hooks/use-create-project";

export function CreateProjectButton() {
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const { createProject, isPending } = useCreateProject();

  const handleCreate = () => {
    if (!title.trim() || !selectedFile) return;
    createProject(
      { title: title.trim(), file: selectedFile },
      {
        onSuccess: () => {
          setTitle("");
          setSelectedFile(null);
          setOpen(false);
        },
        onError: (err) => {
          alert("Failed to create project: " + err.message);
        },
      }
    );
  };

  const handleClose = () => {
    if (isPending) return;
    setTitle("");
    setSelectedFile(null);
    setOpen(false);
  };

  return (
    <>
      <Button variant="contained" onClick={() => setOpen(true)}>
        Create Project
      </Button>

      <Dialog open={open} onClose={handleClose} fullWidth maxWidth="sm">
        <DialogTitle>Create New Project</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Project Title"
            type="text"
            fullWidth
            variant="outlined"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            disabled={isPending}
            sx={{ mb: 2 }}
          />

          <Box sx={{ mt: 1 }}>
            <Typography variant="subtitle2" sx={{ mb: 1 }}>
              Project File (Required)
            </Typography>
            <Button
              component="label"
              variant="outlined"
              disabled={isPending}
              fullWidth
            >
              {selectedFile ? "Change File" : "Choose File"}
              <input
                type="file"
                hidden
                onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                accept=".txt,.pdf,.docx"
              />
            </Button>

            {selectedFile ? (
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Attached: <strong>{selectedFile.name}</strong> ({(selectedFile.size / 1024).toFixed(1)} KB)
              </Typography>
            ) : (
              <Typography variant="caption" color="error" sx={{ mt: 0.5, display: "block" }}>
                * A file must be selected to create a project
              </Typography>
            )}
          </Box>
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 2 }}>
          <Button onClick={handleClose} disabled={isPending}>
            Cancel
          </Button>
          <Button
            onClick={handleCreate}
            variant="contained"
            disabled={isPending || !title.trim() || !selectedFile}
            startIcon={isPending ? <CircularProgress size={16} color="inherit" /> : null}
          >
            {isPending ? "Creating..." : "Create Project"}
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
