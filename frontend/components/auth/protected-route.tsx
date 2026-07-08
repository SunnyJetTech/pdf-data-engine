"use client";

import { useAppSelector } from "@/store/hooks";

export default function ProtectedRoute({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, hydrated, } = useAppSelector((state) => state.auth);

  if (!hydrated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        Loading...
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        Session expired. Please login again.
      </div>
    );
  }

  return <>{children}</>;
}