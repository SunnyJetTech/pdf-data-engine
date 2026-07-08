import { useMutation } from "@tanstack/react-query"
import apiClient from "@/lib/axios"

export function useUploadPdf() {
  return useMutation({
    mutationFn: async (formData: FormData) => {
      const res = await apiClient.post(
        "/pdf/upload",
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }
      )

      return res.data
    },
  })
}