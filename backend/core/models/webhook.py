from __future__ import annotations
import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import BaseModel

if TYPE_CHECKING:
    from core.models.tenant import Tenant
    from core.models.webhook_delivery import WebhookDelivery


class Webhook(BaseModel):
    __tablename__ = "webhooks"

    tenant_id: Mapped[uuid.UUID] = mapped_column( ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column( String(150), nullable=False)
    url: Mapped[str] = mapped_column( String(1000), nullable=False)
    secret: Mapped[str] = mapped_column( String(1024), nullable=False)
    events: Mapped[list[str]] = mapped_column( JSON, default=list, nullable=False)
    active: Mapped[bool] = mapped_column( Boolean, default=True, nullable=False)
    description: Mapped[str | None] = mapped_column( String(500), nullable=True)
    retry_count: Mapped[int] = mapped_column( Integer, default=3, nullable=False)
    timeout_seconds: Mapped[int] = mapped_column( Integer, default=30, nullable=False)
    failure_count: Mapped[int] = mapped_column( Integer, default=0, nullable=False)
    last_delivery_at: Mapped[datetime | None] = mapped_column( DateTime(timezone=True), nullable=True)
    
    tenant: Mapped["Tenant"] = relationship( back_populates="webhooks")
    deliveries: Mapped[list["WebhookDelivery"]] = relationship( back_populates="webhook", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("ix_webhook_tenant_active", "tenant_id", "active"),
    )