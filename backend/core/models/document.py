from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=True)
    mongo_collection = Column(String(255), unique=True, nullable=False)
    rows_count = Column(Integer, default=0)
    columns_count = Column(Integer, default=0)
    has_header = Column(Boolean, default=True)
    status = Column(String(30), default="READY")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="documents")
    searches = relationship("SearchHistory", back_populates="document", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="document", cascade="all, delete-orphan")