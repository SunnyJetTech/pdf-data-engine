import { apiClient } from "@/lib/axios";
import {
  ApiResponse,
  AuthResponse,
  LoginRequest,
  RegisterRequest,
  ChangePasswordRequest,
  ForgotPasswordRequest,
  ResetPasswordRequest,
  CurrentUser,
} from "@/types/api.types";

export const loginUser = async (payload: LoginRequest) => {
  const { data } = await apiClient.post<ApiResponse<AuthResponse>>( "/user/login", payload);

  return data;
};

export const registerUser = async (payload: RegisterRequest) => {
  const { data } = await apiClient.post<ApiResponse>("/user/register", payload);

  return data;
};

export const logoutUser = async () => {
  const { data } = await apiClient.post<ApiResponse>("/user/logout");

  return data;
};

export const getCurrentUser = async () => {
  const { data } = await apiClient.get<ApiResponse<CurrentUser>>("/user/me");

  return data;
};

export const changePassword = async (payload: ChangePasswordRequest) => {
  const { data } = await apiClient.post<ApiResponse>("/user/change-password", payload);

  return data;
};

export const forgotPassword = async (payload: ForgotPasswordRequest) => {
  const { data } = await apiClient.post<ApiResponse>("/user/forgot-password", payload);

  return data;
};

export const resetPassword = async (token: string, payload: ResetPasswordRequest) => {
  const { data } = await apiClient.post<ApiResponse>(`/user/reset-password/${token}`, payload);

  return data;
};