import { useQuery } from "@tanstack/react-query";
import { getAccessToken } from "@/shared/cookies";
import { API_URL } from "@/shared/url";
import { Project } from "../types";

export const useGetProjectById = (projectId: string | null) => {
  const tkn = getAccessToken();

  const { data, isError, error, isLoading } = useQuery<Project>({
    queryKey: ["project", projectId, tkn],
    queryFn: async () => {
      const res = await fetch(`${API_URL}/project/${projectId}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${tkn}`,
        },
      });

      if (!res.ok) {
        throw new Error("Failed to fetch project");
      }

      return res.json();
    },
    enabled: !!projectId && !!tkn,
    refetchInterval: 5000,
  });

  return { project: data, isError, error, isLoading };
};
