from __future__ import annotations
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.constants.payment import PaymentProvider, PaymentStatus
from core.models.payment import Payment
from core.models.pricing_plan import PricingPlan
from core.models.tenant import Tenant
from repositories.payment_repository import PaymentRepository
from services.subscription.subscription_service import SubscriptionService

class PaymentService:
    def __init__(self, db: Session) -> None:
        self.db = db

        self.payments = PaymentRepository(db)
        self.subscriptions = SubscriptionService(db)

    def by_id(self, payment_id: UUID) -> Payment:
        payment = self.payments.by_id(payment_id)

        if payment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found.")

        return payment

    def by_reference(self, reference: str) -> Payment:
        payment = self.payments.by_reference(reference)

        if payment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found.")

        return payment

    def latest(self, tenant_id: UUID) -> Payment | None:
        return self.payments.latest(tenant_id)

    def history(self, tenant_id: UUID) -> list[Payment]:
        return self.payments.by_tenant(tenant_id)

    def pending(self) -> list[Payment]:
        return self.payments.pending()

    def create(self, *, tenant: Tenant, plan: PricingPlan, provider: PaymentProvider, reference: str) -> Payment:

        if self.payments.exists_reference(reference):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Duplicate payment reference.")

        payment = Payment(
            tenant_id=tenant.id,
            amount=plan.amount,
            currency=plan.currency,
            provider=provider,
            reference=reference,
            status=PaymentStatus.PENDING,
        )

        self.payments.add(payment)
        self.db.commit()
        self.db.refresh(payment)

        return payment

    def mark_success(self, *, payment: Payment, transaction_id: str) -> Payment:
        self.payments.mark_success( payment, transaction_id=transaction_id)

        self.db.commit()
        self.db.refresh(payment)

        return payment

    def mark_failed(self, *, payment: Payment) -> Payment:
        self.payments.mark_failed(payment)

        self.db.commit()
        self.db.refresh(payment)

        return payment

    def cancel(self, payment: Payment) -> Payment:
        self.payments.mark_cancelled(payment)

        self.db.commit()
        self.db.refresh(payment)

        return payment

    def verify_success(self, *, payment: Payment, transaction_id: str, plan: PricingPlan) -> Payment:
        if payment.status == PaymentStatus.SUCCESS:
            return payment

        self.payments.mark_success(payment, transaction_id=transaction_id)
        subscription = self.subscriptions.current(payment.tenant_id)

        self.subscriptions.change_plan(subscription=subscription, plan=plan)
        payment.subscription_id = subscription.id

        self.db.commit()
        self.db.refresh(payment)

        return payment

    def total_successful_amount(self, tenant_id: UUID) -> int:
        return self.payments.total_successful_amount(tenant_id)

    def successful_count(self, tenant_id: UUID) -> int:
        return self.payments.count_successful(tenant_id)