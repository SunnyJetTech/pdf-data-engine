import { apiClient } from "@/lib/axios";
import { ApiResponse, SearchRequest, SearchResponse, SearchHistory } from "@/types/api.types";

export const searchDocument = async (payload: SearchRequest) => {
  const { data } = await apiClient.post<ApiResponse<SearchResponse>>("/search", payload);

  return data;
};

export const getSearchHistory = async () => {
  const { data } = await apiClient.get<ApiResponse<SearchHistory[]>>("/search/history");

  return data;
};