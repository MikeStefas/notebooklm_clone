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
      ); //get post url
      const successful = await uploadToS3(upload_url, fields, file); //upload to s3 through url
      if (!successful) {
        throw new Error("Failed to upload file");
      }
      await updateFileStatus(projectId, file_created.id, tkn);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["project", projectId] });
    },
  });

  return { uploadFile: mutate, isError, error, isPending };
};

async function getPresignedURL(file: File, projectId: string, tkn: string) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(
    `${API_URL}/project/${projectId}/file/presigned-url`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${tkn}`,
      },
      body: formData,
    }
  );

  if (!res.ok) {
    throw new Error("Failed to upload file");
  }

  const data = await res.json();
  const upload_url = data.url;
  const fields = data.fields;

  if (!upload_url || !fields) {
    throw new Error("Failed to get presigned POST details");
  }

  return { upload_url, fields, file_created: data.file_created };
}

async function uploadToS3(
  upload_url: string,
  fields: Record<string, string>,
  file: File
) {
  // TODO: REMOVE THIS WHEN FINISH DOCKER
  if (upload_url.includes("http://minio:9000")) {
    upload_url = upload_url.replace(
      "http://minio:9000",
      "http://localhost:9000"
    );
  }

  const s3FormData = new FormData();
  for (const key in fields) {
    s3FormData.append(key, fields[key]);
  }
  s3FormData.append("file", file);

  const uploadRes = await fetch(upload_url, {
    method: "POST",
    body: s3FormData,
  });

  if (!uploadRes.ok) {
    throw new Error("Failed to upload file");
  }

  return true;
}

async function updateFileStatus(
  projectId: string,
  fileId: string,
  tkn: string
) {
  const res = await fetch(
    `${API_URL}/project/${projectId}/file/${fileId}/update-status`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${tkn}`,
      },
    }
  );

  if (!res.ok) {
    throw new Error("Failed to update file status");
  }

  return await res.json();
}
