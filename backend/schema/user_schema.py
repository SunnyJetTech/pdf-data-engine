from pydantic import BaseModel, EmailStr, model_validator

class ForgotPasswordRequest(BaseModel):
    email: EmailStr
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def validate_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")

        return self

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    @model_validator(mode="after")
    def validate_password(self):
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match")

        return self

class ResetPasswordRequest(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def validate_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")

        return self