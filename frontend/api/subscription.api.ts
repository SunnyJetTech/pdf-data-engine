import { apiClient } from "@/lib/axios";
import { ApiResponse } from "@/types/api.types";

export async function getSubscription() {
  const response = await apiClient.get<ApiResponse<any>>("/subscriptions/me");

  return response.data;
}

export async function createCheckout(plan: string) {
  const response = await apiClient.post<ApiResponse<any>>("/subscriptions/checkout", {plan,});

  return response.data;
}