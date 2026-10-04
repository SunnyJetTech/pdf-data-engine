from __future__ import annotations
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class WebhookCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    url: str = Field(min_length=1, max_length=1000)
    events: list[str] = Field(default_factory=list)
    description: str | None = Field(default=None, max_length=500)
    retry_count: int = Field(default=3, ge=0, le=20)
    timeout_seconds: int = Field(default=30, ge=1, le=300)

class WebhookUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    url: str | None = Field(default=None, min_length=1, max_length=1000)
    events: list[str] | None = None
    description: str | None = Field(default=None, max_length=500)
    retry_count: int | None = Field(default=None, ge=0, le=20)
    timeout_seconds: int | None = Field(default=None, ge=1, le=300)

class WebhookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    url: str
    events: list[str]
    active: bool
    description: str | None
    retry_count: int
    timeout_seconds: int
    failure_count: int
    last_delivery_at: datetime | None
    created_at: datetime
    updated_at: datetime

class WebhookCreatedResponse(WebhookResponse):

    secret: str

class WebhookSecretRotationResponse(WebhookResponse):

    secret: str