import { getCookie, setCookie } from "typescript-cookie";

export async function saveTokens(accessToken: string, refreshToken: string) {
  setCookie("access_token", accessToken, { path: "/" });
  setCookie("refresh_token", refreshToken, { path: "/" });
}

export async function clearTokens() {
  setCookie("access_token", "", { path: "/" });
  setCookie("refresh_token", "", { path: "/" });
}

export function getAccessToken() {
  const token = getCookie("access_token");
  if (!token || token === "undefined" || token === "null") {
    return undefined;
  }
  return token;
}

export function getRefreshToken() {
  const token = getCookie("refresh_token");
  if (!token || token === "undefined" || token === "null") {
    return undefined;
  }
  return token;
}
