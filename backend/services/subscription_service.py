from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from core.Models import Subscription

def activate_subscription(db: Session, user_id: int, plan_name: str, duration_days: int = 30):
    existing_subscription = db.query(Subscription).filter(Subscription.user_id == user_id, Subscription.is_active == True).first()
    
    if existing_subscription:
        existing_subscription.is_active = False
        
    subscription = Subscription(
        user_id=user_id,
        plan_name=plan_name,
        is_active = True,
        start_date=datetime.utcnow(),
        expiry_date=datetime.utcnow() + timedelta(days=duration_days)
    )
    
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    
    return subscription

