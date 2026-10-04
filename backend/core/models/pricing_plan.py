from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import BaseModel

if TYPE_CHECKING:
    from .subscription import Subscription

class PricingPlan(BaseModel):
    __tablename__ = "pricing_plans"

    name: Mapped[str] = mapped_column( String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column( String(500), nullable=True)
    amount: Mapped[int] = mapped_column( Integer, nullable=False)
    currency: Mapped[str] = mapped_column( String(10), default="NGN", nullable=False)
    duration_days: Mapped[int] = mapped_column( Integer, default=30, nullable=False)
    display_order: Mapped[int] = mapped_column( Integer, default=0, nullable=False)
    trial_days: Mapped[int] = mapped_column( Integer, default=0, nullable=False)
    is_default: Mapped[bool] = mapped_column( Boolean, default=False, nullable=False)
    active: Mapped[bool] = mapped_column( Boolean, default=True, nullable=False)
    api_access: Mapped[bool] = mapped_column( Boolean, default=False, nullable=False)
    priority_processing: Mapped[bool] = mapped_column( Boolean, default=False, nullable=False)
    features: Mapped[dict] = mapped_column( JSON, default=dict, nullable=False)
    
    subscriptions: Mapped[list["Subscription"]] = relationship( back_populates="plan", cascade="all, delete-orphan")