export interface UploadProgress {
  current_page: number
  total_pages: number
  percentage: number
}

export interface UploadProgressMessage {
  type?: string
  status?: string
  current_page?: number
  total_pages?: number
  percentage?: number
  message?: string
}

export interface UploadResponse {
  status: string
  message: string
  data?: {
    rows: number
    columns: number
    collection?: string
    file?: string
  }
}