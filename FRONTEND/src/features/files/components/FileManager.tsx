import {
  Box,
  Typography,
  Button,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";
import { useUploadFile } from "@/features/files/hooks/use-upload-file";
import { useDeleteFile } from "@/features/files/hooks/use-delete-file";
import { Project } from "@/features/projects/types";

interface FileManagerProps {
  projectId: string;
  files?: Project["files"];
  selectedFileId?: string | null;
  onSelectFile?: (fileId: string | null) => void;
}

export default function FileManager({
  projectId,
  files,
  selectedFileId,
  onSelectFile,
}: FileManagerProps) {
  const { uploadFile, isPending: uploading } = useUploadFile(projectId);
  const { deleteFile, isPending: deleting } = useDeleteFile(projectId);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    uploadFile(file, {
      onSuccess: () => {
        alert("success");
      },
      onError: (err) => {
        alert("Upload failed: " + err.message);
      },
    });
  };

  const handleFileDelete = (fileId: string) => {
    deleteFile(fileId, {
      onSuccess: () => {
        alert("success");
      },
      onError: (err) => {
        alert("Delete failed: " + err.message);
      },
    });
  };

  return (
    <>
      <Typography variant="h6">Sources</Typography>

      <Box sx={{ my: 2 }}>
        <Button component="label" variant="contained" disabled={uploading}>
          {uploading ? "Uploading..." : "Add file"}
          <input
            type="file"
            hidden
            onChange={handleFileUpload}
            accept=".txt,.pdf,.docx"
          />
        </Button>
      </Box>

      <List sx={{ flexGrow: 1, overflowY: "auto" }}>
        {files && files.length > 0 ? (
          files.map((file) => (
            <ListItem
              key={file.id}
              secondaryAction={
                <Button
                  size="small"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleFileDelete(file.id);
                  }}
                  disabled={deleting}
                  color="error"
                >
                  Delete
                </Button>
              }
              disablePadding
            >
              <Button
                onClick={() =>
                  onSelectFile?.(selectedFileId === file.id ? null : file.id)
                }
                sx={{
                  width: "100%",
                  textAlign: "left",
                  justifyContent: "flex-start",
                  textTransform: "none",
                  color: "text.primary",
                  py: 1,
                  px: 1.5,
                  borderRadius: 1,
                  bgcolor:
                    selectedFileId === file.id
                      ? "action.selected"
                      : "transparent",
                  "&:hover": {
                    bgcolor: "action.hover",
                  },
                }}
              >
                <ListItemText
                  primary={file.name}

                  sx={{ pr: 6 }}
                />
              </Button>
            </ListItem>
          ))
        ) : (
          <Typography>No sources uploaded yet.</Typography>
        )}
      </List>
    </>
  );
}
