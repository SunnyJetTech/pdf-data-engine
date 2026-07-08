from pydantic import BaseModel

class ExportRequest(BaseModel):
    document_id: int
    column: str | None = None
    operator: str | None = None
    value: str | None = None
    
