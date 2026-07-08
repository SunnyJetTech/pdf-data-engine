import { useMutation, useQueryClient } from "@tanstack/react-query"
import { deleteDocument } from "@/api/document.api"

export function useDeleteDocument() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: deleteDocument,

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["documents"],
      })
    },
  })
}