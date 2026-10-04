from pydantic import BaseModel, EmailStr

class UpdateUserRequest(BaseModel):
    email: EmailStr
    data: dict