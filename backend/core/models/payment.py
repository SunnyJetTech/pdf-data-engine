from datetime import datetime
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String)
from sqlalchemy.orm import relationship
from db.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer,  primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(String(50))
    currency = Column(String(10), default="NGN")
    reference = Column(String(255), unique=True)
    status = Column(String(50), default="pending")
    plan_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="payments")