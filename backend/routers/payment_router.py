import uuid
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from db.database import get_db, SessionLocal
from core.Models import User, Payment
from core.functions import get_current_user_from_cookie
from services.paystack_service import initialize_payment, verify_paystack_signature, verify_payment
from services.subscription_service import activate_subscription


router = APIRouter(
    prefix='/payments',
    tags=['PAYMENTS']
)

@router.post("/initialize")
def initialize_subscription_payment(sub_amount: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    reference = str(uuid.uuid4())
    
    payment = Payment(
        user_id=current_user.id,
        amount=sub_amount,
        reference=reference,
        status="pending"
    )
    
    db.add(payment)
    db.commit()
    
    result = initialize_payment(
        email=current_user.email,
        amount=sub_amount,
        reference=reference
    )
    
    return result

@router.get('/verify/{reference}')
def verify_transaction(reference: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.reference==reference).first()
    
    if not payment:
        return {
            "stastus": False,
            "message": "Payment not found"
        }
        
    result = verify_payment(reference)
    
    if result['status'] and result['data']['status'] == 'success':
        payment.status = "success"
        db.commit()
        
        return {
            "status": True,
            "message": "Payment verified" 
        }
        
    return {
        "status": False,
        "message": "Payment failed"
    }
    
@router.post('/webhook')
async def paystack_webhook(request: Request):
    payload = await request.body()
    
    signature = request.headers.get("x-paystack-signature")
    
    if not signature:
        raise HTTPException(status_code=400, detail='Missing signature')
    
    if not verify_paystack_signature(payload, signature):
        raise HTTPException(status_code=400, detail='Invalid signature')
    
    event = await request.json()
    event_type = event.get('event')
    
    if event_type != 'charge.success':
        return {"status": "ignored"}
    
    Payment_data = event['data']
    reference = event['reference']
    
    db: Session = SessionLocal()
    
    try:
        payment = db.query(Payment).filter(Payment.reference == reference).first()
        
        if not payment:
            return {"status": "Payment_not_found"}
        
        if payment.status == "success":
            return {"status": "already_processed"}
        
        payment.status = "success"
        
        activate_subscription(
            db=db,
            user_id=payment.user_id,
            plan_name="Premium",
            duration_days=30
        )
        
        db.commit()
        return {"status": "success"}
    finally:
        db.close()