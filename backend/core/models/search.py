from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    column_name = Column(String(255), nullable=False)
    operator = Column(String(50), nullable=False)
    search_value = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="searches")
    document = relationship("Document", back_populates="searches")
    