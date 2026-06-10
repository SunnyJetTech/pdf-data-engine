export interface ProgressMessage {
    type?: string
    status?: string
    current_page?: number
    total_pages?: number
    percentage?: number
    rows?: number
    file?: string
    collection?: string
    message?: string
}