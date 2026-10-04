import { apiClient } from "@/lib/axios";
import {ApiResponse, Documents, DocumentStats} from "@/types/api.types";

export const getAllDocuments = async () => {
  const { data } = await apiClient.get<ApiResponse<Documents[]>>("/documents");

  return data;
};

export const getSingleDocument = async (documentId: number) => {
  const { data } = await apiClient.get<ApiResponse<Documents>>(`/documents/${documentId}`);

  return data;
};

export const getDocumentColumns = async (documentId: number) => {
  const { data } = await apiClient.get<ApiResponse<string[]>>(`/documents/${documentId}/columns`);

  return data;
};

export const getDocumentSample = async (documentId: number) => {
  const { data } = await apiClient.get<ApiResponse>(`/documents/${documentId}/sample`);

  return data;
};

export const getDocumentStatistics = async (documentId: number) => {
  const { data } = await apiClient.get<ApiResponse<DocumentStats>>(`/documents/${documentId}/stats`);

  return data;
};

export const deleteDocument = async (documentId: number) => {
  const { data } = await apiClient.delete<ApiResponse>(`/documents/${documentId}`);

  return data;
};