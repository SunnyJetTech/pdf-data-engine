from __future__ import annotations
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base

class Quota(Base):
    __tablename__ = "quotas"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    uploads_used: Mapped[int] = mapped_column(Integer, default=0)
    uploads_limit: Mapped[int] = mapped_column(Integer, default=5)
    searches_used: Mapped[int] = mapped_column(Integer, default=0)
    searches_limit: Mapped[int] = mapped_column(Integer, default=100)

    user = relationship("User", back_populates="quota")