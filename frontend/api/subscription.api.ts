import { apiClient } from "@/lib/axios";
import {ApiResponse, Subscription, PricingPlan, CheckoutResponse} from "@/types/api.types";

export const getPlans = async () => {
  const { data } = await apiClient.get<ApiResponse<PricingPlan[]>>("/subscriptions/plans");

  return data;
};

export const getSubscription = async () => {
  const { data } = await apiClient.get<ApiResponse<Subscription | null>>("/subscriptions/me");

  return data;
};

export const createCheckout = async (plan: string) => {
  const { data } = await apiClient.post<ApiResponse<CheckoutResponse>>( "/subscriptions/checkout", null, {params: {plan,},});

  return data;
};