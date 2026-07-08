import { useQuery } from "@tanstack/react-query"
import { getSingleDocument } from "@/api/document.api"
import { QUERY_KEYS } from "@/lib/query-keys"

export function useDocument(
  documentId: number
) {
  return useQuery({
    queryKey: QUERY_KEYS.document(documentId),

    queryFn: () =>
      getSingleDocument(documentId),

    enabled: !!documentId,
  })
}