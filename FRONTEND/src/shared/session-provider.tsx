"use client";
import { useRouter, usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { getAccessToken } from "./cookies";

export default function SessionProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const [authorized, setAuthorized] = useState<boolean | null>(null);

  useEffect(() => {
    const checkSession = () => {
      const tkn = getAccessToken();

      if (!tkn) {
        setAuthorized(false);
        router.replace("/");
      } else {
        setAuthorized(true);
      }
    };
    checkSession();
  }, [router, pathname]);

  if (authorized === null || authorized == false) {
    return null;
  }

  return <>{children}</>;
}
