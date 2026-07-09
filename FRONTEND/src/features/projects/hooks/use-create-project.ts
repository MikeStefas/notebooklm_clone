import { useMutation, useQueryClient } from "@tanstack/react-query";
import { API_URL } from "@/shared/url";
import { getAccessToken } from "@/shared/cookies";

export const useCreateProject = () => {
  const tkn = getAccessToken();
  const queryClient = useQueryClient();

  const { mutate, isError, error, isPending } = useMutation({
    mutationKey: ["create_project", tkn],
    mutationFn: async (title: string) => {
      const res = await fetch(`${API_URL}/project`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${tkn}`,
        },
        body: JSON.stringify({ title }),
      });

      if (!res.ok) {
        throw new Error("Failed to create project");
      }

      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["all_projects", tkn] });
    },
  });

  return { createProject: mutate, isError, error, isPending };
};
