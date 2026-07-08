import axios from "axios";
import { store } from "@/store";
import { clearUser } from "@/store/slices/authSlice";

export const apiClient = axios.create({
    baseURL:
      process.env.NEXT_PUBLIC_API_URL,
    withCredentials: true,
  });

apiClient.interceptors.response.use(
  (response) => response,

  (error) => {
    const status = error?.response?.status;

    if (status === 401) {
      store.dispatch(
        clearUser()
      );

      const path = window.location.pathname;

      const authPages = [
        "/login",
        "/register",
        "/forgot-password",
        "/reset-password",
      ];

      const isAuthPage = authPages.some((page) =>
          path.startsWith(page)
        );

      if (!isAuthPage) {
        window.location.replace(
          "/login"
        );
      }
    }

    return Promise.reject(
      error
    );
  }
);

export default apiClient;