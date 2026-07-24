import { Box, Typography, Button } from "@mui/material";
import { useUploadFile } from "@/features/files/hooks/use-upload-file";
import { useDeleteFile } from "@/features/files/hooks/use-delete-file";
import { ProjectFile } from "@/features/projects/types";

interface FileManagerProps {
  projectId: string;
  file?: ProjectFile | null;
  selectedFileId?: string | null;
  onSelectFile?: (fileId: string | null) => void;
}

export default function FileManager({
  projectId,
  file,
  selectedFileId,
  onSelectFile,
}: FileManagerProps) {
  const { uploadFile, isPending: uploading } = useUploadFile(projectId);
  const { deleteFile, isPending: deleting } = useDeleteFile(projectId);

  const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected) uploadFile(selected);
  };

  return (
    <Box>
      <Typography variant="h6">Project Source</Typography>

      {file ? (
        <Box sx={{ mt: 1 }}>
          <Typography
            variant="body2"
            onClick={() => onSelectFile?.(selectedFileId === file.id ? null : file.id)}
            sx={{ cursor: "pointer", fontWeight: selectedFileId === file.id ? 700 : 400 }}
          >
            {file.name} ({file.status})
          </Typography>

          <Box sx={{ mt: 1, display: "flex", gap: 1 }}>
            <Button component="label" size="small" variant="outlined" disabled={uploading || deleting}>
              {uploading ? "Replacing..." : "Replace"}
              <input type="file" hidden onChange={handleUpload} accept=".txt,.pdf,.docx" />
            </Button>

            <Button
              size="small"
              color="error"
              disabled={uploading || deleting}
              onClick={() => {
                deleteFile(file.id, { onSuccess: () => onSelectFile?.(null) });
              }}
            >
              {deleting ? "Deleting..." : "Delete"}
            </Button>
          </Box>
        </Box>
      ) : (
        <Box sx={{ mt: 1 }}>
          <Typography variant="body2" color="text.secondary">No file attached.</Typography>
          <Button component="label" size="small" variant="contained" sx={{ mt: 1 }} disabled={uploading}>
            {uploading ? "Uploading..." : "Upload File"}
            <input type="file" hidden onChange={handleUpload} accept=".txt,.pdf,.docx" />
          </Button>
        </Box>
      )}
    </Box>
  );
}
