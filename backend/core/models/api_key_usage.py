from __future__ import annotations
import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import BaseModel

if TYPE_CHECKING:
    from core.models.api_key import APIKey
    from core.models.tenant import Tenant


class APIKeyUsage(BaseModel):
    __tablename__ = "api_key_usage"

    api_key_id: Mapped[uuid.UUID] = mapped_column( ForeignKey("api_keys.id", ondelete="CASCADE"), nullable=False, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column( ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    request_id: Mapped[str | None] = mapped_column( String(100), nullable=True, index=True)
    endpoint: Mapped[str] = mapped_column( String(500), nullable=False)
    http_method: Mapped[str] = mapped_column( String(10), nullable=False)
    status_code: Mapped[int] = mapped_column( Integer, nullable=False)
    response_time_ms: Mapped[int | None] = mapped_column( Integer, nullable=True)
    request_bytes: Mapped[int | None] = mapped_column( Integer, nullable=True)
    response_bytes: Mapped[int | None] = mapped_column( Integer, nullable=True)
    ip_address: Mapped[str | None] = mapped_column( String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column( String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column( DateTime(timezone=True), nullable=False)
    api_key: Mapped["APIKey"] = relationship()

    tenant: Mapped["Tenant"] = relationship()

    __table_args__ = (
        Index( "ix_api_key_usage_tenant_created", "tenant_id", "created_at"),
        Index( "ix_api_key_usage_key_created", "api_key_id", "created_at"),
    )