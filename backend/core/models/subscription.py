from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_id = Column(Integer, ForeignKey("pricing_plans.id"))
    is_active = Column(Boolean, default=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)

    user = relationship("User", back_populates="subscriptions")
    plan = relationship("PricingPlan")
 
class PricingPlan(Base):
    __tablename__ = "pricing_plans"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    amount = Column(Integer, nullable=False)  # amount in kobo
    currency = Column(String(10), default="NGN")
    duration_days = Column(Integer, nullable=False, default=30)
    uploads_limit = Column(Integer, nullable=False)
    searches_limit = Column(Integer, nullable=False)
    max_file_size_mb = Column(Integer, nullable=False)
    priority_processing = Column(Boolean, default=False)
    api_access = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)