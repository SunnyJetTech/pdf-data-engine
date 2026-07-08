"use client";

import { useRouter } from "next/navigation";
import { useDispatch } from "react-redux";
import { logoutUser } from "@/api/auth.api";
import { clearUser } from "@/store/slices/authSlice";
import { useAppSelector } from "@/store/hooks";

export default function LogoutButton() {
  const router = useRouter();
  const dispatch = useDispatch();

  const user = useAppSelector(
    (state) => state.auth.user
  );

  if (!user) {
    return null;
  }

  async function handleLogout() {
    try {
      await logoutUser();
    } catch (error) {
      console.error(error);
    } finally {
      dispatch(clearUser());

      router.replace("/");
    }
  }

  return (
    <button
      onClick={handleLogout}
      className="text-red-500 text-sm"
    >
      Logout
    </button>
  );
}