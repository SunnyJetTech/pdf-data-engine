import { useQuery } from "@tanstack/react-query"
import { getAllDocuments } from "@/api/document.api"

export function useDocuments() {
  return useQuery({
    queryKey: ["documents"],
    queryFn: getAllDocuments,
  })
} 