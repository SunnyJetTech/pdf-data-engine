import apiClient from "@/lib/axios";
import { ApiResponse, UploadPdfResponse  } from "@/types/api.types"

export async function uploadPdf(
    file: File,
    clientId: string,
    saveMode: string,
    hasHeader = true
) {
    const formData = new FormData()

    formData.append("file", file)
    formData.append("client_id", clientId)
    formData.append("save_mode", saveMode)
    formData.append("has_header", String(hasHeader))

    const response = await apiClient.post<ApiResponse<UploadPdfResponse>>(
        "/pdf/upload", 
        formData, {headers : {"Content-Type": "multipart/form-data"},}
    )

    return response.data
}