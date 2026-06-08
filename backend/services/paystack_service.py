import requests
from core.config import settings
import hmac
import hashlib

BASE_URL = "https://api.paystack.co"

def initialize_payment(email: str, amount: int, reference: str):
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "email": email,
        "amount": amount,
        "reference": reference,
        "callback_url": settings.PAYSTACK_CALLBACK_URL
    }
    
    response = requests.post(
        f"{BASE_URL}/transaction/initialize",
        json=payload,
        headers=headers
    )
    
    return response.json()

def verify_payment(reference: str):
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }
    
    response = requests.get(
        f"{BASE_URL}/transaction/verify/{reference}",
        headers=headers
    )
    
    return response.json()

def verify_paystack_signature(payload: bytes, signature: str) -> bool:
    computed_signature = hmac.new(
        settings.PAYSTACK_SECRET_KEY,
        payload,
        hashlib.sha512
    ).hexdigest()
    
    return hmac.compare_digest(
        computed_signature,
        signature
    )
    
