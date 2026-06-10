import apiClient from "@/lib/axios";
import { ApiResponse } from "@/types/api.types"
import { UserResponse, DocumentResponse } from "@/types/admin.types"

export async function getUsers() {
    const response = await apiClient.get<ApiResponse<UserResponse[]>>("/admin/users")

    return response.data
}

export async function getUser(id: number) {
    const response = await apiClient.get<ApiResponse<UserResponse>>(`/admin/users/${id}`)

    return response.data
}

export async function deleterUser(id: number) {
    const response = await apiClient.delete<ApiResponse>(`/admin/users/${id}/delete`)

    return response.data
}

export async function getDocuments() {
    const response = await apiClient.get<ApiResponse<DocumentResponse[]>>("/admin/documents")

    return response.data
}

export async function getSingleDocument(user_id: number) {
    const response = await apiClient.get<ApiResponse<DocumentResponse[]>>(`/admin/documents/${user_id}`)

    return response.data
}

export async function deleteDocument(document_id: number) {
    const response = await apiClient.delete<ApiResponse>(`/admin/documents/${document_id}/delete`)

    return response.data
}
