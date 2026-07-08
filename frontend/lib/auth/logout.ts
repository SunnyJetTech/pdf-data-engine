import { logoutUser } from "@/api/auth.api";
import { notify } from "@/lib/notify";

export async function handleLogout(router?: any) {
  try {
    await logoutUser();

    notify.success("Logged out successfully");

    if (router) {
      router.replace("/login");
    } else {
      window.location.href = "/login";
    }
  } catch (err) {
    notify.error(err);
  }
}