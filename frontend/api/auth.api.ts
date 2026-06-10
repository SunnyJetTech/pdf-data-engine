import apiClient from "@/lib/axios";
import { 
  ApiResponse, 
  LoginResponse, 
  LoginRequest,
  RegisterRequest,
  ChangePasswordRequest,
  CurrentUser
} from "@/types/api.types";

export async function login(payload: LoginRequest) {
  const response = await apiClient.post<ApiResponse<LoginResponse>>(
      "/user/login",
      payload
    );

  return response.data;
}

export async function register(payload: RegisterRequest) {
  const response = await apiClient.post<ApiResponse>(
    "/user/register",
    payload
  );

  return response.data
}

export async function logout() {
  const response = await apiClient.post<ApiResponse>('/user/logout')

  return response.data
}

export async function changePassword(payload: ChangePasswordRequest) {
  const response = await apiClient.post<ApiResponse>(
    "/user/change-password",
    payload
  )
  
  return response.data
}

export async function forgotPassword(payload: string) {
  const response = await apiClient.post<ApiResponse>(
    "/user/change-password",
    payload
  )
  
  return response.data
}

export async function resetPassword(token: string, payload: ChangePasswordRequest) {
  const response = await apiClient.post<ApiResponse>(
    `/user/reset-password/${token}`,
    payload
  )

  return response.data
}

export async function getCurrentUser() {
  const response =
    await apiClient.get<ApiResponse<CurrentUser>>(
      "/user/me"
    )

  return response.data
}

