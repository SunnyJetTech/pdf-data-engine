from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, JSON, Index, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import BaseModel
from core.constants.tenant import TenantStatus
import uuid

if TYPE_CHECKING:
    from .tenant_member import TenantMember
    from .user import User
    from .dataset import Dataset
    from .quota import Quota
    from .usage import Usage
    from .payment import Payment
    from .role import Role
    from .invitation import Invitation
    from .api_key import APIKey
    from .webhook import Webhook
    from .subscription import Subscription
    from .activity import Activity


class Tenant(BaseModel):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[TenantStatus] = mapped_column(Enum(TenantStatus), default=TenantStatus.ACTIVE, nullable=False)
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    settings: Mapped[dict] = mapped_column(JSON, default=lambda: {}, nullable=False)
    
    owner: Mapped["User"] = relationship(back_populates="owned_tenants", foreign_keys=[owner_id])
    members: Mapped[list["TenantMember"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")
    datasets: Mapped[list["Dataset"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")
    quota: Mapped["Quota"] = relationship( back_populates="tenant", uselist=False, cascade="all, delete-orphan")
    usage: Mapped["Usage"] = relationship( back_populates="tenant", uselist=False, cascade="all, delete-orphan")
    payments: Mapped[list["Payment"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")
    roles: Mapped[list["Role"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")
    invitations: Mapped[list["Invitation"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")
    api_keys: Mapped[list["APIKey"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")
    webhooks: Mapped[list["Webhook"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")
    activities: Mapped[list["Activity"]] = relationship( back_populates="tenant", cascade="all, delete-orphan")
    subscriptions: Mapped[list["Subscription"]] = relationship( back_populates="tenant", cascade="all, delete-orphan")
    roles: Mapped[list["Role"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")
    
    __table_args__ = (Index("ix_tenant_status", "status"))