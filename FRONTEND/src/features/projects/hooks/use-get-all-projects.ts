import { useQuery } from "@tanstack/react-query";
import { getAccessToken } from "@/shared/cookies";
import { API_URL } from "@/shared/url";
import { Project } from "../types";

export const useGetAllProjects = () => {
  const tkn = getAccessToken();

  const { data, isError, error, isLoading, isSuccess } = useQuery<Project[]>({
    queryKey: ["all_projects", tkn],
    queryFn: async () => {
      const res = await fetch(`${API_URL}/project`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${tkn}`,
        },
      });

      if (!res.ok) {
        throw new Error("Failed to fetch projects");
      }

      return res.json();
    },
    enabled: !!tkn,
  });

  return { projects: data, isError, error, isLoading, isSuccess };
};
