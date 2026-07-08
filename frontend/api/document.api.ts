import { apiClient } from "@/lib/axios";
import {ApiResponse, Documents, SearchDocumentRequest, SearchDocumentResponse,} from "@/types/api.types";

export async function getAllDocuments() {
    const response = await apiClient.get<ApiResponse<Documents[]>>('/documents')

    return response.data
}

export async function getSingleDocument(document_id: number) { 
    const response = await apiClient.get<ApiResponse<Documents>>(`/documents/${document_id}`)

    return response.data
}

export async function SearchDocument(payload: SearchDocumentRequest) {
  const response = await apiClient.post<SearchDocumentResponse>("/documents/search", payload)

  return response.data
}

export async function SearchColumn(documentId: number) {
  const response = await apiClient.get<ApiResponse<string[]>>(`/documents/${documentId}/columns`)

  return response.data
}

export async function deleteDocument(document_id: number) {
    const response = await apiClient.delete<ApiResponse>(`/documents/${document_id}/delete`)

    return response.data
}
