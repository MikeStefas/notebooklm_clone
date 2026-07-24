import { getAccessToken } from "@/shared/cookies";
import { API_URL } from "@/shared/url";
import { Message } from "../types";

export const getAllMessages = async (projectId: string): Promise<Message[]> => {
  const tkn = getAccessToken();
  const res = await fetch(`${API_URL}/project/${projectId}/messages`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${tkn}`,
    },
  });

  if (!res.ok) {
    throw new Error("Failed to fetch project messages");
  }

  return res.json();
};
