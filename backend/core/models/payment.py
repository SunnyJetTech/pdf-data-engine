from __future__ import annotations
import uuid
from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, Enum, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.constants.payment import PaymentProvider, PaymentStatus
from core.models.base import BaseModel

if TYPE_CHECKING:
    from core.models.subscription import Subscription
    from core.models.tenant import Tenant

class Payment(BaseModel):
    __tablename__ = "payments"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    subscription_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("subscriptions.id", ondelete="SET NULL"), nullable=True)
    amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="NGN", nullable=False)
    provider: Mapped[PaymentProvider] = mapped_column(Enum(PaymentProvider), default=PaymentProvider.PAYSTACK, nullable=False)
    reference: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    transaction_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    
    tenant: Mapped["Tenant"] = relationship(back_populates="payments")
    subscription: Mapped["Subscription | None"] = relationship(back_populates="payments")

    __table_args__ = (Index("ix_payment_reference", "reference"), Index("ix_payment_status", "status"))