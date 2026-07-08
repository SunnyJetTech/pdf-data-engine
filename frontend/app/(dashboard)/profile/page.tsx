"use client";

import { useAppSelector } from "@/store/hooks";
import ProfileSkeleton from "@/components/skeletons/profile-skeleton"
 
export default function ProfilePage() {
  const user = useAppSelector(
    (state) => state.auth.user
  );

  if (!user) {
    return <ProfileSkeleton />;
  }

  return (
    <div className="max-w-xl space-y-6">
      <h1 className="text-3xl font-bold">
        Profile
      </h1>

      <div className="border rounded-lg p-6 space-y-3">
        <p>
          <strong>Username:</strong>{" "}
          {user.username ?? "N/A"}
        </p>

        <p>
          <strong>Email:</strong>{" "}
          {user.email}
        </p>

        <p>
          <strong>Role:</strong>{" "}
          {user.is_admin ? "ADMIN" : "User"}
        </p>
      </div>
    </div>
  );
}