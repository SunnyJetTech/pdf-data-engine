from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    # has_active_subscription: bool
    # subscription_date: Optional[str] = None
    # subscription_expiry: Optional[str] = None
    
class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    
    @model_validator(mode="after")
    def validate_request(self):
        if not self.username or not self.email or not self.password or not self.confirm_password:
            raise ValueError("All fields are required")
        
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        
        return self
class LoginInputSchema(BaseModel):
    email: str
    password: str
    
class ChangePasswordSchema(BaseModel):
    password: str
    new_password: str
    confirm_new_password: str
    
    @model_validator(mode='after')
    def validate_password(self):
        if not self.new_password or not self.confirm_new_password:
            raise ValueError("All fields are required")
        
        if self.new_password != self.confirm_new_password:
            raise ValueError("Passwords do not match")
        
        return self
    
class ResetPasswordSchema(BaseModel):
    password: str
    confirm_password: str
    
    @model_validator(mode='after')
    def validate_password(self):
        if not self.password or not self.confirm_password:
            raise ValueError("All fields are required")
        
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        
        return self
    
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