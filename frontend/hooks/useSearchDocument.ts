import { useMutation } from "@tanstack/react-query"
import { SearchDocument } from "@/api/document.api"

export function useSearchDocument() {
  return useMutation({
    mutationFn: SearchDocument,
  })
}