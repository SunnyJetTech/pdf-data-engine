import { apiClient } from "@/lib/axios"

export async function exportCsv(payload: any) {
  const res = await apiClient.post("/documents/export/csv", payload, {responseType: "blob",})

  return res.data
}

export async function exportExcel(payload: any) {
  const res = await apiClient.post("/documents/export/excel", payload, {responseType: "blob",})

  return res.data
}