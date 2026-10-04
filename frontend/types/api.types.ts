export interface ExportRequest {
    document_id: number;
    export_all: boolean;
    column?: string;
    operator?: string;
    value?: string;
}

export interface PricingPlan {
  id: number;
  name: string;
  amount: number;
  duration_days: number;
}

export interface CheckoutResponse {
  plan: string;
  amount: number;
  authorization_url: string;
  reference: string;
}

export interface UploadResponse {
  rows: number;
  columns: number;
  file?: string;
  collection?: string;
}

export interface Subscription {
  id: number;
  plan_name: string;
  is_active: boolean;
  start_date: string;
  expiry_date: string;
}

export interface ApiResponse<T = unknown> {
  status: string;
  message: string;
  data: T | null;
}

export interface DocumentStats {
  rows: number;
  columns: number;
  created_at?: string;
}

export interface ApiError {
  message: string;
  statusCode?: number;
}

export interface SearchRequest {
  document_id: number;
  column: string;
  operator: string;
  value: string;
  page: number;
  page_size: number;
}

export interface SearchResponse {
  total: number;
  page: number;
  page_size: number;
  results: Record<string, unknown>[];
}

export interface SearchHistory {
  id: number;
  document_id: number;
  column: string;
  operator: string;
  value: string;
  created_at: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  confirm_password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface ResetPasswordRequest {
  password: string
  confirmPassword: string
}
export interface ChangePasswordRequest {
  password: string;
  new_password: string;
  confirm_new_password: string;
}
export interface ForgotPasswordRequest {
  email: string
}

export interface AuthResponse {
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

