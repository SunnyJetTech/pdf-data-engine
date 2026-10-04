from __future__ import annotations
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class APIKeyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    expires_at: datetime | None = None

class APIKeyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    key_prefix: str
    created_by: uuid.UUID | None
    created_at: datetime
    last_used_at: datetime | None
    expires_at: datetime | None
    revoked_at: datetime | None
    is_active: bool

class APIKeyCreatedResponse(APIKeyResponse):
    
    plaintext_key: str


class APIKeyRotateResponse(APIKeyCreatedResponse):
    pass