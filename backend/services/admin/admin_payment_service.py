from __future__ import annotations
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from core.models import Payment

class AdminPaymentService:

    @staticmethod
    def serialize(payment: Payment) -> dict:
        return {
            "id": payment.id,
            "user_id": payment.user_id,
            "username": payment.user.username,
            "email": payment.user.email,
            "reference": payment.reference,
            "amount": payment.amount,
            "currency": payment.currency,
            "status": payment.status,
            "plan_name": payment.plan_name,
            "created_at": payment.created_at,
        }

    @classmethod
    def serialize_many(cls, payments: list[Payment]) -> list[dict]:

        return [
            cls.serialize(payment)
            for payment in payments
        ]

    @staticmethod
    def all(db: Session) -> list[Payment]:

        return (db.query(Payment).options(joinedload(Payment.user)).order_by(Payment.created_at.desc()).all())

    @staticmethod
    def get(db: Session, payment_id: int) -> Payment:

        payment = db.query(Payment).options(joinedload(Payment.user)).filter(Payment.id == payment_id).first()

        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found.",
            )

        return payment

    @staticmethod
    def by_user(db: Session, user_id: int) -> list[Payment]:

        return db.query(Payment).options(joinedload(Payment.user)).filter(Payment.user_id == user_id).order_by(Payment.created_at.desc()).all()

    @staticmethod
    def successful(db: Session) -> list[Payment]:

        return db.query(Payment).options(joinedload(Payment.user)).filter(Payment.status == "success").order_by(Payment.created_at.desc()).all()

    @staticmethod
    def pending(db: Session) -> list[Payment]:

        return db.query(Payment).options(joinedload(Payment.user)).filter(Payment.status == "pending").order_by(Payment.created_at.desc()).all()