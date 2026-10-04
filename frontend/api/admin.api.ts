import { apiClient } from "@/lib/axios";
import { ApiResponse } from "@/types/api.types";
import {
  DashboardStats,
  UserResponse,
  DocumentResponse,
  PricingResponse,
  SubscriptionResponse,
  PaymentResponse,
  QuotaResponse,
  RevenueAnalytics,
  UserAnalytics,
  UploadAnalytics,
  SearchAnalytics,
} from "@/types/admin.types";

export const getDashboardStats = async () => {
  const { data } = await apiClient.get<ApiResponse<DashboardStats>>("/admin/dashboard");

  return data;
};

export const getUsers = async () => {
  const { data } = await apiClient.get<ApiResponse<UserResponse[]>>("/admin/users");

  return data;
};

export const getUser = async (userId: number) => {
  const { data } = await apiClient.get<ApiResponse<UserResponse>>(`/admin/users/${userId}`);

  return data;
};

export const deleteUser = async (userId: number) => {
  const { data } = await apiClient.delete<ApiResponse>(`/admin/users/${userId}`);

  return data;
};

export const getDocuments = async () => {
  const { data } = await apiClient.get<ApiResponse<DocumentResponse[]>>("/admin/documents");

  return data;
};

export const getUserDocuments = async (userId: number) => {
  const { data } = await apiClient.get<ApiResponse<DocumentResponse[]>>(`/admin/documents/user/${userId}`);

  return data;
};

export const deleteDocument = async (documentId: number) => {
  const { data } = await apiClient.delete<ApiResponse>(`/admin/documents/${documentId}`);

  return data;
};

export const getPricingPlans = async () => {
  const { data } = await apiClient.get<ApiResponse<PricingResponse[]>>("/admin/pricing");

  return data;
};

export const createPricingPlan = async (payload: any) => {
  const { data } = await apiClient.post<ApiResponse>("/admin/pricing", payload);

  return data;
};

export const updatePricingPlan = async (pricingId: number, payload: any) => {
  const { data } = await apiClient.put<ApiResponse>(`/admin/pricing/${pricingId}`, payload);

  return data;
};

export const deletePricingPlan = async (pricingId: number) => {
  const { data } = await apiClient.delete<ApiResponse>(`/admin/pricing/${pricingId}`);

  return data;
};

export const getSubscriptions = async () => {
  const { data } = await apiClient.get<ApiResponse<SubscriptionResponse[]>>("/admin/subscriptions");

  return data;
};

export const getSubscription = async (subscriptionId: number) => {
  const { data } = await apiClient.get<ApiResponse<SubscriptionResponse>>(`/admin/subscriptions/${subscriptionId}`);

  return data;
};

export const cancelSubscription = async (subscriptionId: number) => {
  const { data } = await apiClient.post<ApiResponse>(`/admin/subscriptions/${subscriptionId}/cancel`);

  return data;
};

export const activateSubscription = async (subscriptionId: number) => {
  const { data } = await apiClient.post<ApiResponse>(`/admin/subscriptions/${subscriptionId}/activate`);

  return data;
};

export const deleteSubscription = async (subscriptionId: number) => {
  const { data } = await apiClient.delete<ApiResponse>(`/admin/subscriptions/${subscriptionId}`);

  return data;
};

export const getPayments = async () => {
  const { data } = await apiClient.get<ApiResponse<PaymentResponse[]>>("/admin/payments");

  return data;
};

export const getPayment = async (paymentId: number) => {
  const { data } = await apiClient.get<ApiResponse<PaymentResponse>>(`/admin/payments/${paymentId}`);

  return data;
};

export const getUserPayments = async (userId: number) => {
  const { data } = await apiClient.get<ApiResponse<PaymentResponse[]>>(`/admin/payments/user/${userId}`);

  return data;
};

export const getSuccessfulPayments = async () => {
  const { data } = await apiClient.get<ApiResponse<PaymentResponse[]>>("/admin/payments/successful");

  return data;
};

export const getPendingPayments = async () => {
  const { data } = await apiClient.get<ApiResponse<PaymentResponse[]>>("/admin/payments/pending");

  return data;
};

export const getQuotas = async () => {
  const { data } = await apiClient.get<ApiResponse<QuotaResponse[]>>("/admin/quotas");

  return data;
};

export const getQuota = async (userId: number) => {
  const { data } = await apiClient.get<ApiResponse<QuotaResponse>>(`/admin/quotas/${userId}`);

  return data;
};

export const createQuota = async (userId: number, uploadsLimit: number, searchesLimit: number) => {
  const { data } = await apiClient.post<ApiResponse>("/admin/quotas", null, {
      params: {
        user_id: userId,
        uploads_limit: uploadsLimit,
        searches_limit: searchesLimit,
      },
    });

  return data;
};

export const updateQuota = async (userId: number, uploadsLimit: number, searchesLimit: number) => {
  const { data } = await apiClient.put<ApiResponse>(`/admin/quotas/${userId}`, null,
      {
        params: {
          uploads_limit: uploadsLimit,
          searches_limit: searchesLimit,
        },
      }
    );

  return data;
};

export const resetQuota = async (userId: number) => {
  const { data } = await apiClient.put<ApiResponse>(`/admin/quotas/${userId}/reset`);

  return data;
};

export const deleteQuota = async (userId: number) => {
  const { data } = await apiClient.delete<ApiResponse>(`/admin/quotas/${userId}`);

  return data;
};

export const getRevenueAnalytics = async () => {
  const { data } = await apiClient.get<ApiResponse<RevenueAnalytics>>("/admin/analytics/revenue");

  return data;
};

export const getUserGrowthAnalytics = async () => {
  const { data } = await apiClient.get<ApiResponse<UserAnalytics>>("/admin/analytics/users");

  return data;
};

export const getUploadAnalytics = async () => {
  const { data } = await apiClient.get<ApiResponse<UploadAnalytics>>("/admin/analytics/uploads");

  return data;
};

export const getSearchAnalytics = async () => {
  const { data } = await apiClient.get<ApiResponse<SearchAnalytics>>("/admin/analytics/searches");

  return data;
};