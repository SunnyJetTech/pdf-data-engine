import { apiClient } from "@/lib/axios";
import { 
  ApiResponse, 
  LoginResponse, 
  LoginRequest,
  RegisterRequest,
  ChangePasswordRequest,
  CurrentUser,
  ForgotPasswordRequest,
  ResetPasswordRequest
} from "@/types/api.types";

export async function loginUser(payload: LoginRequest) {
  const response = await apiClient.post<ApiResponse<LoginResponse>>("/user/login", payload);
  
  return response.data;
}

export async function registerUser(payload: RegisterRequest) {
  const response = await apiClient.post<ApiResponse>("/user/register", payload);

  return response.data
}

export async function logoutUser() {
  const response = await apiClient.post("/user/logout")

  return response.data
}

export async function changePassword(payload: ChangePasswordRequest) {
  const response = await apiClient.post<ApiResponse>("/user/change-password", payload)
  
  return response.data
}

export async function forgotPassword(payload: ForgotPasswordRequest) {
  const response = await apiClient.post<ApiResponse>("/user/change-password", payload)
  
  return response.data
}

export async function resetPassword(token: string, payload: ResetPasswordRequest) {
  const response = await apiClient.post<ApiResponse>(`/user/reset-password/${token}`, payload)

  return response.data
}

export async function getCurrentUser() {
  const response =
    await apiClient.get<ApiResponse<CurrentUser>>("/user/me")

  return response.data
}

export async function getMe() {
  const res = await apiClient.get("/user/me")
  
  return res.data
}

export async function getProfile() {
  const response = await apiClient.get<ApiResponse<LoginResponse>>("/user/profile")

  return response.data
}

