import { API_URL } from "@/shared/url";
import { useMutation } from "@tanstack/react-query";
import { saveTokens } from "@/shared/cookies";

export const useSignUp = () => {
  const {
    mutate: signUpMutation,
    error: signUpError,
    isPending: isSignUpPending,
    isSuccess: isSignUpSuccess,
  } = useMutation({
    mutationKey: ["sign-up"],
    mutationFn: async ({
      email,
      password,
      username,
    }: {
      email: string;
      password: string;
      username: string;
    }) => {
      const response = await fetch(`${API_URL}/auth/sign_up`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password, username }),
      });
      if (!response.ok) {
        throw new Error("Failed to sign up");
      }
      const body = await response.json();
      await saveTokens(body.access_token, body.refresh_token);
      return body;
    },
  });

  return { signUpMutation, signUpError, isSignUpPending, isSignUpSuccess };
};
