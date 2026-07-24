import { useQuery } from "@tanstack/react-query";
import { getAllMessages } from "../api/get-all-messages";
import { Message } from "../types";
import { useEffect, useState } from "react";

export const useGetAllMessages = (projectId: string) => {
  const [displayedMessages, setDisplayedMessages] = useState<Message[]>([]);

  const {
    data: messages,
    isError: isGetAllMessagesError,
    error: getAllMessagesError,
    isLoading: isGetAllMessagesLoading,
    isSuccess: isGetAllMessagesSuccess,
    refetch: refetchGetAllMessages,
  } = useQuery<Message[]>({
    queryKey: ["all_messages", projectId],
    queryFn: () => getAllMessages(projectId),
    enabled: !!projectId,
  });

  //sync messages into the stateful var displayedMessages
  //export a setter so other components can add messages
  useEffect(() => {
    if (messages) {
      const syncMessages = () => {
        setDisplayedMessages(messages);
      };
      syncMessages();
    }
  }, [messages]);

  return {
    displayedMessages,
    setDisplayedMessages,
    isGetAllMessagesError,
    getAllMessagesError,
    isGetAllMessagesLoading,
    isGetAllMessagesSuccess,
    refetchGetAllMessages,
  };
};
