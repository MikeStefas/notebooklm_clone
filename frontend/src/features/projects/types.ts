export interface ProjectFile {
  id: string;
  name: string;
  nextcloud_path?: string;
  status: "pending" | "uploaded" | "processing" | "processed" | "failed";
  created_at: string;
  updated_at: string;
}

export interface Project {
  id: string;
  title: string;
  user_id: string;
  created_at: string;
  updated_at: string;
  file?: ProjectFile | null;
}
