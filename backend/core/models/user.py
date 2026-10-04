from typing import TYPE_CHECKING
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from core.models.base import BaseModel
from core.models.tenant import Tenant

if TYPE_CHECKING:
    from .activity import Activity
    from .conversation_memory import Conversation
    from .dataset import Dataset
    from .payment import Payment
    from .quota import Quota
    from .search import SearchHistory
    from .subscription import Subscription
    from .tenant_member import TenantMember
    from .document import Document
    from .search import SavedSearch
    from .invitation import Invitation
    from .refresh_token import RefreshToken
    from .chat_session import ChatSession

class User(BaseModel):

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    tenant_memberships: Mapped[list["TenantMember"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    subscriptions: Mapped[list["Subscription"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    payments: Mapped[list["Payment"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    quota: Mapped["Quota"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    search_history: Mapped[list["SearchHistory"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    activities: Mapped[list["Activity"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    conversation_memory: Mapped[list["Conversation"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    datasets: Mapped[list["Dataset"]] = relationship(back_populates="created_by_user")
    documents: Mapped[list["Document"]] = relationship(back_populates="created_by_user")
    chat_sessions: Mapped[list["ChatSession"]] = relationship(back_populates="created_by_user", cascade="all, delete-orphan")
    saved_searches: Mapped[list["SavedSearch"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    owned_tenants: Mapped[list["Tenant"]] = relationship(foreign_keys="Tenant.owner_id")
    sent_invitations: Mapped[list["Invitation"]] = relationship(foreign_keys="Invitation.invited_by_id")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user", cascade="all, delete-orphan")