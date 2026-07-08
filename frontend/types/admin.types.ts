export interface UserResponse {
  id: number
  email: string
  full_name: string
  is_active: boolean
  role: string
  created_at: string
}

export interface DocumentResponse {
  id: number
  filename: string
  rows_count: number
  uploaded_at: string
  owner_id: number
}

export interface DashboardStats {
  users: number
  documents: number
  searches: number
  revenue: number
}

export interface SubscriptionResponse {
  id: number
  user_id: number
  plan: string
  status: string
  expires_at: string
}