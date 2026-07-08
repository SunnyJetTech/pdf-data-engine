from datetime import datetime
from pydantic import BaseModel

class SubscriptionResponse(BaseModel):
    plan_name: str
    is_active: bool
    start_date: datetime
    expiry_date: datetime