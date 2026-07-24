export type Message = {
  id: string;
  projectId: string;
  role: "USER" | "AI";
  content: string;
  createdAt: string;
  updatedAt: string;
};
