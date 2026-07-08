import { useQuery } from "@tanstack/react-query"
import { getCurrentUser } from "@/api/auth.api"
import { QUERY_KEYS } from "@/lib/query-keys"

export function useCurrentUser() {
  return useQuery({
    queryKey: QUERY_KEYS.me,

    queryFn: getCurrentUser,
  })
}