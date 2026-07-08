export const QUERY_KEYS = {
  me: ["me"],
  documents: ["documents"],
  document: (id: number) => ["document", id],
  search: (payload: any) => ["search", payload],
}