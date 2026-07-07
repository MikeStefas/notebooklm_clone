import { getCookie, setCookie } from "typescript-cookie";

export async function saveTokens(accessToken: string, refreshToken: string) {
  setCookie("access_token", accessToken);
  setCookie("refresh_token", refreshToken);
}

export async function clearTokens() {
  setCookie("access_token", "");
  setCookie("refresh_token", "");
}

export async function getAccessToken() {
  return getCookie("access_token");
}

export async function getRefreshToken() {
  return getCookie("refresh_token");
}
