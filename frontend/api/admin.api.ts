import { apiClient } from "@/lib/axios"
import { ApiResponse } from "@/types/api.types"
import {UserResponse, DocumentResponse, DashboardStats, SubscriptionResponse,} from "@/types/admin.types"

export async function getDashboardStats() {
  const response =await apiClient.get<ApiResponse<DashboardStats>>("/admin/dashboard")

  return response.data
}

export async function getUsers() {
  const response = await apiClient.get<ApiResponse<UserResponse[]>>("/admin/users")

  return response.data
}

export async function getUser(id: number) {
  const response = await apiClient.get<ApiResponse<UserResponse>>(`/admin/users/${id}`)

  return response.data
}

export async function deleteUser(id: number) {
  const response = await apiClient.delete<ApiResponse>(`/admin/users/${id}/delete`)

  return response.data
}

export async function getDocuments() {
  const response = await apiClient.get<ApiResponse<DocumentResponse[]>>("/admin/documents")

  return response.data
}

export async function deleteDocument(documentId: number) {
  const response = await apiClient.delete<ApiResponse>(`/admin/documents/${documentId}/delete`)

  return response.data
}

export async function getSubscriptions() {
  const response = await apiClient.get<ApiResponse<SubscriptionResponse[]>>("/admin/subscriptions")

  return response.data
}

export async function cancelSubscription(subscriptionId: number) {
  const response = await apiClient.post<ApiResponse>(`/admin/subscriptions/${subscriptionId}/cancel`)

  return response.data
}

export async function getRevenueAnalytics() {
  const response = await apiClient.get("/admin/analytics/revenue")

  return response.data
}

export async function getUserGrowthAnalytics() {
  const response = await apiClient.get("/admin/analytics/users")

  return response.data
}

export async function getUploadAnalytics() {
  const response = await apiClient.get("/admin/analytics/uploads")

  return response.data
}

export async function getSearchAnalytics() {
  const response = await apiClient.get("/admin/analytics/searches")

  return response.data
}

