export interface UserResponse {
    id: string
    username: string
    email: string
    is_admin: string
    is_active: string
}

export interface DocumentResponse {
    id: string
    user_id: number
    filename: string
    mongo_collection: string
    rows_count: number
    columns_count: number
    created_at: string
}

