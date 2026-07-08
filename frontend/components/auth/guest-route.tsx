"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAppSelector } from "@/store/hooks";

export default function GuestRoute({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();

  const { user, hydrated, } = useAppSelector((state) => state.auth);

  useEffect(() => {
    if (!hydrated) return;

    if (user) {
      router.replace(
        "/dashboard"
      );
    }
  }, [
    user,
    hydrated,
    router,
  ]);

  if (!hydrated) {
    return null;
  }

  if (user) {
    return null;
  }

  return <>{children}</>;
}