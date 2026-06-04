from pydantic import BaseModel, EmailStr
from typing import Optional

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    has_active_subscription: bool
    subscription_date: Optional[str] = None
    subscription_expiry: Optional[str] = None

class APIResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[dict] = None

class OptionalUserResponse(BaseModel):
    status: str
    message: str
    data: Optional[UserOut] = None

class AdminCheckResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict] = None