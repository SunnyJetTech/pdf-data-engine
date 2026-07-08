import { apiClient } from "@/lib/axios";
import { 
    ApiResponse, 
} from "@/types/api.types";

export async function initialpayment(amount: number) {
    const response = await apiClient.post<ApiResponse>('/payments/initialize', amount)

    return response.data 
}

export async function verifyPayment(reference: string) {
    const response = await apiClient.get<ApiResponse>(`/payments/verify/${reference}`)

    return response.data
}