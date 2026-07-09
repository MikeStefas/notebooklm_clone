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

      const res = await fetch(`${API_URL}/project/${projectId}/file`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${tkn}`,
        },
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Failed to upload file");
      }

      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["project", projectId] });
    },
  });

  return { uploadFile: mutate, isError, error, isPending };
};
