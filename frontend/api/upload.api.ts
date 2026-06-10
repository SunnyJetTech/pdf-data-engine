import apiClient from "@/lib/axios";
import { ApiResponse, UploadPdfResponse  } from "@/types/api.types"
import { UploadPdtRequest } from "@/types/file.types"

export async function uploadPdf(payload: UploadPdtRequest) {
    const formData = new FormData()

    formData.append("client_id", payload.client_id)
    formData.append("file", payload.file)
    formData.append("has_header", String(payload.has_header))
    formData.append("save_mode", payload.save_mode)

    const response = await apiClient.post<ApiResponse<UploadPdfResponse>>(
        "/pdf/upload", 
        formData, {headers : {"Content-Type": "multipart/form-data"},}
    )

    return response.data
}