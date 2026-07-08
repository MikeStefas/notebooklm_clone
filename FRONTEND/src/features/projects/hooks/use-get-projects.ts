import { useQuery } from "@tanstack/react-query";
import { getAccessToken } from "@/shared/cookies";
import { API_URL } from "@/shared/url";
import { Project } from "../types";

export const useGetProjects = () => {
  const tkn = getAccessToken();
  return useQuery<Project[]>({
    queryKey: ["projects", tkn],
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
};
