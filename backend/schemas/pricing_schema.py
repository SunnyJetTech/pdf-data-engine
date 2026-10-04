from pydantic import BaseModel

class InitializePaymentRequest(BaseModel):
    plan_name: str

class PaymentResponse(BaseModel):
    authorization_url: str
    reference: str

class PricingCreate(BaseModel):
    name: str
    amount: int
    description: str | None = None

class PricingUpdate(BaseModel):
    name: str | None = None
    amount: int | None = None
    description: str | None = None
    active: bool | None = None