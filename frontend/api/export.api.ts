import { apiClient } from "@/lib/axios";
import { ExportRequest } from "@/types/api.types";

export const exportCsv = async (payload: ExportRequest) => {
  const { data } = await apiClient.post("/export/csv", payload, { responseType: "blob"});

  return data;
};

export const exportExcel = async (payload: ExportRequest) => {
  const { data } = await apiClient.post("/export/excel", payload, { responseType: "blob" });

  return data;
};