import { getAccessToken } from "@/shared/cookies";
import { API_URL } from "@/shared/url";

export const postMessageApi = async (projectId: string, content: string) => {
  const tkn = getAccessToken();
  const res = await fetch(`${API_URL}/project/${projectId}/messages/user`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${tkn}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content }),
  });

  if (!res.ok) {
    throw new Error("Failed to post message");
  }

  return res.json();
};
