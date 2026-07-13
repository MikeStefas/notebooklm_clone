import { useMutation, useQueryClient } from "@tanstack/react-query";
import { getAccessToken } from "@/shared/cookies";
import { API_URL } from "@/shared/url";

export const useUploadFile = (projectId: string | null) => {
  const tkn = getAccessToken();
  const queryClient = useQueryClient();

  const { mutate, isError, error, isPending } = useMutation({
    mutationKey: ["upload_file", projectId, tkn],
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${API_URL}/project/${projectId}/file/upload`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${tkn}`,
        },
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Failed to upload file");
      }

      const data = await res.json();
      let upload_url = data.url;
      const fields = data.fields;

      if (!upload_url || !fields) {
        throw new Error("Failed to get presigned POST details");
      }

      // TODO: REMOVE THIS WHEN FINISH DOCKER
      if (upload_url.includes("http://minio:9000")) {
        upload_url = upload_url.replace("http://minio:9000", "http://localhost:9000");
      }

      const s3FormData = new FormData();
      Object.entries(fields).forEach(([key, val]) => {
        s3FormData.append(key, val as string);
      });
      s3FormData.append("file", file);

      const uploadRes = await fetch(upload_url, {
        method: "POST",
        body: s3FormData,
      });

      if (!uploadRes.ok) {
        throw new Error("Failed to upload file");
      }

      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["project", projectId] });
    },
  });

  return { uploadFile: mutate, isError, error, isPending };
};
