from __future__ import annotations
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any
from sqlalchemy import  Boolean, DateTime, ForeignKey, Index, Integer, JSON, String, Text,
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import BaseModel

if TYPE_CHECKING:
    from core.models.webhook import Webhook

class WebhookDelivery(BaseModel):
    __tablename__ = "webhook_deliveries"

    webhook_id: Mapped[uuid.UUID] = mapped_column( ForeignKey("webhooks.id", ondelete="CASCADE"), nullable=False, index=True)
    event: Mapped[str] = mapped_column( String(100), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column( JSON, nullable=False)
    http_status: Mapped[int | None] = mapped_column( Integer, nullable=True)
    response_body: Mapped[str | None] = mapped_column( Text, nullable=True)
    error_message: Mapped[str | None] = mapped_column( Text, nullable=True)
    duration_ms: Mapped[int | None] = mapped_column( Integer, nullable=True)
    attempt: Mapped[int] = mapped_column( Integer, default=1, nullable=False)
    success: Mapped[bool] = mapped_column( Boolean, default=False, nullable=False)
    next_retry_at: Mapped[datetime | None] = mapped_column( DateTime(timezone=True), nullable=True, index=True)
    delivered_at: Mapped[datetime | None] = mapped_column( DateTime(timezone=True), nullable=True)
    
    webhook: Mapped["Webhook"] = relationship( back_populates="deliveries")
    
    __table_args__ = (
        Index("ix_webhook_delivery_retry", "webhook_id", "success", "next_retry_at"),
    )