import { useGetAllMessages } from "./use-get-messages";
import { Message } from "../types";
import { useMutation } from "@tanstack/react-query";
import { postMessageApi } from "../api/post-message";

export const useHandleSendMessage = ({
  projectId,
  inputValue,
  setInputValue,
}: {
  projectId: string;
  inputValue: string;
  setInputValue: (val: string) => void;
}) => {
  const { mutate: postMessage, isPending: isPostMessagePending } = useMutation({
    mutationFn: (content: string) => postMessageApi(projectId, content),
  });

  const {
    displayedMessages,
    setDisplayedMessages,
    isGetAllMessagesLoading,
    isGetAllMessagesError,
    getAllMessagesError,
  } = useGetAllMessages(projectId);

  const handleSendMessage = () => {
    if (!inputValue.trim() || isPostMessagePending) return;

    const messageText = inputValue;
    setInputValue("");

    const userMsg: Message = {
      id: `USER-${Date.now()}`,
      projectId: projectId,
      role: "USER",
      content: messageText,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    setDisplayedMessages((prev) => [...prev, userMsg]);

    postMessage(messageText, {
      onSuccess: (data) => {
        console.log("Search Results:", data);

        const AIMsg: Message = {
          id: `AI-${Date.now()}`,
          projectId: projectId,
          role: "AI",
          content: data,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        };
        setDisplayedMessages((prev) => [...prev, AIMsg]);
      },
      onError: (error) => {
        console.error("Failed to post message:", error);
      },
    });
  };

  return {
    handleSendMessage,
    displayedMessages,
    isGetAllMessagesLoading,
    isGetAllMessagesError,
    getAllMessagesError,
    isPostMessagePending,
  };
};
