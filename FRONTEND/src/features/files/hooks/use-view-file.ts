import { useQuery } from "@tanstack/react-query";
import { getAccessToken } from "@/shared/cookies";
import { API_URL } from "@/shared/url";

export const useViewFile = (
  projectId: string | null,
  fileId: string | null
) => {
  const tkn = getAccessToken();

  const { data, isError, error, isPending } = useQuery({
    queryKey: ["project", projectId, "file", fileId, tkn],
    queryFn: async () => {
      const res = await fetch(
        `${API_URL}/project/${projectId}/file/${fileId}/presigned-url`,
        {
          headers: {
            Authorization: `Bearer ${tkn}`,
          },
        }
      );

      if (!res.ok) {
        throw new Error("Failed to get presigned URL");
      }

      const data = await res.json();
      if (data.url.includes("http://minio:9000")) {
        data.url = data.url.replace(
          "http://minio:9000",
          "http://localhost:9000"
        );
      }
      return data.url;
    },
    enabled: !!projectId && !!fileId,
  });

  return { url: data, isError, error, isPending };
};
