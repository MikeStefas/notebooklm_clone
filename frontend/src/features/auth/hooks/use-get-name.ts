import { getAccessToken } from "@/shared/cookies";
import { jwtDecode } from "jwt-decode";
import { CustomJwtPayload } from "@/shared/typs";

export const useGetName = () => {
  const tkn = getAccessToken();
  if (!tkn) return null;
  console.log("Token:", tkn);
  try {
    const decoded = jwtDecode<CustomJwtPayload>(tkn);
    return decoded.username;
  } catch (error) {
    console.error("Failed to decode token:", error);
    return null;
  }
};
