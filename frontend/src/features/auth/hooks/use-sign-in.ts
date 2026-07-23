"use client";

import { useMutation } from "@tanstack/react-query";
import { API_URL } from "@/shared/url";
import { saveTokens } from "@/shared/cookies";

export const useSignIn = () => {
  const {
    mutate: signInMutation,
    error: signInError,
    isPending: isSignInPending,
  } = useMutation({
    mutationKey: ["sign-in"],
    mutationFn: async ({ email, password }: Record<string, string>) => {
      const params = new URLSearchParams();
      params.append("username", email);
      params.append("password", password);

      const response = await fetch(`${API_URL}/auth/sign_in`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: params,
      });
      if (!response.ok) {
        throw new Error("Failed to sign in");
      }
      const body = await response.json();
      await saveTokens(body.access_token, body.refresh_token);

      return body;
    },
  });

  return { signInMutation, signInError, isSignInPending };
};
