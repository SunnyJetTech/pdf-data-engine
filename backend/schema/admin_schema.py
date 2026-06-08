from pydantic import BaseModel
from typing import List

class APIResponse(BaseModel):
    status: str
    message: str
    data: List | None = None
    
class UsersOutputSchema(APIResponse):
    data: List | None = None
    
class UpdateUserDataInputSchema(BaseModel):
    email: str
    data: object