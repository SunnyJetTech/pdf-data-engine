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

