import { useMutation, useQueryClient } from "@tanstack/react-query";
import { getAccessToken } from "@/shared/cookies";
import { API_URL } from "@/shared/url";

export const useUploadFile = (projectId: string) => {
  const tkn = getAccessToken();
  if (!tkn) {
    throw new Error("No token found");
  }
  const queryClient = useQueryClient();

  const { mutate, isError, error, isPending } = useMutation({
    mutationKey: ["upload_file", projectId, tkn],
    mutationFn: async (file: File) => {
      const { upload_url, fields, file_created } = await getPresignedURL(
        file,
        projectId,
        tkn
      );
      const successful = await uploadToS3(upload_url, fields, file);
      if (!successful) {
        throw new Error("Failed to upload file to storage server");
      }
      await confirmUpload(projectId, file_created.id, tkn);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["project", projectId] });
    },
  });

  return { uploadFile: mutate, isError, error, isPending };
};

async function getPresignedURL(file: File, projectId: string, tkn: string) {
  let res: Response;
  try {
    res = await fetch(
      `${API_URL}/project/${projectId}/file/presigned-url`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${tkn}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          filename: file.name,
          content_type: file.type || "application/octet-stream",
        }),
      }
    );
  } catch (err: any) {
    console.error("Presigned URL network error:", err);
    throw new Error(`Failed to request presigned URL (${err?.message || "Network Error"})`);
  }

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to get presigned upload URL (HTTP ${res.status}: ${text})`);
  }

  const data = await res.json();
  const upload_url = data.url;
  const fields = data.fields;

  if (!upload_url || !fields) {
    throw new Error("Invalid presigned POST details returned");
  }

  return { upload_url, fields, file_created: data.file_created };
}

async function uploadToS3(
  upload_url: string,
  fields: Record<string, string>,
  file: File
) {
  let finalUrl = upload_url
    .replace("http://minio:9000", "http://localhost:9000")
    .replace("http://127.0.0.1:9000", "http://localhost:9000");

  const s3FormData = new FormData();
  for (const key in fields) {
    s3FormData.append(key, fields[key]);
  }
  s3FormData.append("file", file);

  let uploadRes: Response;
  try {
    uploadRes = await fetch(finalUrl, {
      method: "POST",
      body: s3FormData,
    });
  } catch (err: any) {
    console.error("S3 upload network error:", err);
    throw new Error(`Failed to connect to file storage server (${err?.message || "Network Error"})`);
  }

  if (!uploadRes.ok) {
    const s3Err = await uploadRes.text().catch(() => "");
    throw new Error(`File storage rejected upload (HTTP ${uploadRes.status}: ${s3Err})`);
  }

  return true;
}

async function confirmUpload(
  projectId: string,
  fileId: string,
  tkn: string
) {
  let res: Response;
  try {
    res = await fetch(
      `${API_URL}/project/${projectId}/file/${fileId}/confirm-upload`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${tkn}`,
        },
      }
    );
  } catch (err: any) {
    console.error("Confirm upload network error:", err);
    throw new Error(`Failed to connect to backend for confirm upload (${err?.message})`);
  }

  if (!res.ok) {
    throw new Error(`Failed to confirm file upload (HTTP ${res.status})`);
  }

  return await res.json();
}
