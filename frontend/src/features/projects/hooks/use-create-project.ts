import { useMutation, useQueryClient } from "@tanstack/react-query";
import { API_URL } from "@/shared/url";
import { getAccessToken } from "@/shared/cookies";

export interface CreateProjectParams {
  title: string;
  file: File;
}

export const useCreateProject = () => {
  const tkn = getAccessToken();
  const queryClient = useQueryClient();

  const { mutate, isError, error, isPending } = useMutation({
    mutationKey: ["create_project", tkn],
    mutationFn: async ({ title, file }: CreateProjectParams) => {
      if (!tkn) throw new Error("No authorization token found");

      let res: Response;
      try {
        res = await fetch(`${API_URL}/project/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${tkn}`,
          },
          body: JSON.stringify({
            title,
            filename: file.name,
            content_type: file.type || "application/octet-stream",
          }),
        });
      } catch (err: any) {
        console.error("Project creation network error:", err);
        throw new Error(`Failed to connect to backend server (${err?.message || "Network Error"})`);
      }

      if (!res.ok) {
        const errorText = await res.text().catch(() => "");
        throw new Error(`Failed to create project (HTTP ${res.status}: ${errorText || res.statusText})`);
      }

      const projectData = await res.json();
      const { id: projectId, file: fileCreated, upload_url, fields } = projectData;

      if (upload_url && fields && fileCreated) {
        let finalUploadUrl = upload_url
          .replace("http://minio:9000", "http://localhost:9000")
          .replace("http://127.0.0.1:9000", "http://localhost:9000");

        const s3FormData = new FormData();
        for (const key in fields) {
          s3FormData.append(key, fields[key]);
        }
        s3FormData.append("file", file);

        let uploadRes: Response;
        try {
          uploadRes = await fetch(finalUploadUrl, {
            method: "POST",
            body: s3FormData,
          });
        } catch (err: any) {
          console.error("S3 upload network error:", err);
          throw new Error(`Failed to upload file to storage server (${err?.message || "Network Error"})`);
        }

        if (!uploadRes.ok) {
          const s3Err = await uploadRes.text().catch(() => "");
          throw new Error(`File storage upload rejected (HTTP ${uploadRes.status}: ${s3Err || uploadRes.statusText})`);
        }

        let confirmRes: Response;
        try {
          confirmRes = await fetch(
            `${API_URL}/project/${projectId}/file/${fileCreated.id}/confirm-upload`,
            {
              method: "POST",
              headers: {
                Authorization: `Bearer ${tkn}`,
              },
            }
          );
        } catch (err: any) {
          console.error("Confirm upload network error:", err);
          throw new Error(`Failed to confirm upload with backend (${err?.message || "Network Error"})`);
        }

        if (!confirmRes.ok) {
          throw new Error(`Backend confirm upload failed (HTTP ${confirmRes.status})`);
        }
      }

      return projectData;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["all_projects", tkn] });
    },
  });

  return { createProject: mutate, isError, error, isPending };
};
