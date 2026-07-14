import { useMutation, useQueryClient } from "@tanstack/react-query";
import { getAccessToken } from "@/shared/cookies";
import { API_URL } from "@/shared/url";

export const useDeleteFile = (projectId: string | null) => {
  const tkn = getAccessToken();
  const queryClient = useQueryClient();

  const { mutate, isError, error, isPending } = useMutation({
    mutationKey: ["delete_file", projectId, tkn],
    mutationFn: async (fileId: string) => {
      const res = await fetch(
        `${API_URL}/project/${projectId}/file/${fileId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${tkn}`,
          },
        }
      );

      if (!res.ok) {
        throw new Error("Failed to delete file");
      }

      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["project", projectId] });
    },
  });

  return { deleteFile: mutate, isError, error, isPending };
};
