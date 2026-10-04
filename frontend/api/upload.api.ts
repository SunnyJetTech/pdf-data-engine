import { apiClient } from "@/lib/axios";
import { ApiResponse, UploadResponse } from "@/types/api.types";

export const uploadDocument = async (file: File, clientId: string, hasHeader: boolean, saveMode: "database" | "excel" | "none") => {

  const formData = new FormData();

  formData.append("file", file);
  formData.append("client_id", clientId);
  formData.append("has_header", String(hasHeader));
  formData.append("save_mode", saveMode);

  const { data } = await apiClient.post<ApiResponse<UploadResponse>>("/pdf/upload", formData,
      {
        headers: { "Content-Type":"multipart/form-data"},
      }
    );

  return data;
};