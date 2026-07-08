export type SaveMode = 
    | "database"
    | "excel"
    | "none"

export interface UploadPdtRequest {
    client_id: string
    file: File
    has_header: boolean
    save_mode: SaveMode
}

export interface Document {
  id: number
  filename: string
  mongo_collection: string
  rows_count: number
  columns_count: number
  created_at: string
}

export interface DocumentsResponse {
  status: string
  message: string
  data: Document[]
}

export interface SearchDocumentPayload {
  document_id: number
  column: string
  operator: string
  value: string
  page?: number
  page_size?: number
}