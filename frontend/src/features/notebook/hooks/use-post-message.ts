import { useMutation, useQueryClient } from "@tanstack/react-query";
import { getAccessToken } from "@/shared/cookies";
import { API_URL } from "@/shared/url";

export const usePostMessage = (projectId: string | null) => {
  const queryClient = useQueryClient();

  const {
    mutate: postMessage,
    error: postMessageError,
    isPending: isPostMessagePending,
    isSuccess: isPostMessageSuccess,
  } = useMutation({
    mutationFn: async (content: string) => {
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
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["messages", projectId] });
    },
  });

  return {
    postMessage,
    postMessageError,
    isPostMessagePending,
    isPostMessageSuccess,
  };
};
