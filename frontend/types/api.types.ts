
export interface ApiResponse<T = unknown> {
  status: string;
  message: string;
  data: T | null;
}

export interface ApiError {
  message: string;
  statusCode?: number;
}

export interface RegisterRequest {
  email: string;
  username: string;
  confirm_password: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface ChangePasswordRequest {
  password: string;
  new_password: string;
  confirm_new_password: string
}

export interface LoginResponse {
  user_id: number;
  username: string;
  email: string;
  is_active: boolean;
  is_admin: boolean;
}

export interface CurrentUser {
  id: number
  username: string
  email: string
  is_active: boolean
  is_admin: boolean
}

export interface Documents {
  id: number;
  filename: string;
  mongo_collection: string;
  rows: number;
  columns: number;
  created_at: string;
}

export interface SearchDocumentRequest {
  document_id: number
  column: string
  operator:
    | "="
    | "contains"
    | "startswith"
    | "endswith"
    | ">"
    | "<"
    | ">="
    | "<="

  value: string
  page: number
  page_size: string 
}

export interface SearchDocumentResponse {
  total: number
  page: number
  page_size: number
  results: Record<string, unknown>[]
}

export interface UploadPdfResponse {
  document_id?: number
  filename: string
  collection?: string
  rows: number
  columns: number
  file?: string
}

