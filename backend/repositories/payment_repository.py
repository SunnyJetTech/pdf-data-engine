from __future__ import annotations
import uuid
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session, joinedload
from core.constants.payment import PaymentStatus
from core.models.payment import Payment
from repositories.base_repository import BaseRepository

class PaymentRepository(BaseRepository[Payment]):

    def __init__(self, db: Session):
        super().__init__(db=db, model=Payment)

    def by_id(self, payment_id: uuid.UUID) -> Payment | None:
        stmt = select(Payment).options(joinedload(Payment.subscription)).where(Payment.id == payment_id)

        return self.db.scalar(stmt)

    def by_reference(self, reference: str) -> Payment | None:
        stmt = select(Payment).options(joinedload(Payment.subscription)).where(Payment.reference == reference)

        return self.db.scalar(stmt)

    def by_transaction_id(self, transaction_id: str) -> Payment | None:
        stmt = select(Payment).where(Payment.transaction_id == transaction_id)

        return self.db.scalar(stmt)

    def by_tenant(self, tenant_id: uuid.UUID) -> list[Payment]:
        stmt = select(Payment).where(Payment.tenant_id == tenant_id).order_by(desc(Payment.created_at))

        return list(self.db.scalars(stmt).all())

    def pending(self) -> list[Payment]:
        stmt = select(Payment).where(Payment.status == PaymentStatus.PENDING).order_by(Payment.created_at)

        return list(self.db.scalars(stmt).all())

    def successful(self, tenant_id: uuid.UUID) -> list[Payment]:
        stmt = (
            select(Payment)
            .where(Payment.tenant_id == tenant_id, Payment.status == PaymentStatus.SUCCESS)
            .order_by(desc(Payment.created_at))
        )

        return list(self.db.scalars(stmt).all())

    def failed(self, tenant_id: uuid.UUID) -> list[Payment]:
        stmt = (
            select(Payment)
            .where(Payment.tenant_id == tenant_id, Payment.status == PaymentStatus.FAILED)
            .order_by(desc(Payment.created_at))
        )

        return list(self.db.scalars(stmt).all())

    def latest(self, tenant_id: uuid.UUID) -> Payment | None:
        stmt = (
            select(Payment)
            .where(Payment.tenant_id == tenant_id)
            .order_by(desc(Payment.created_at))
            .limit(1)
        )

        return self.db.scalar(stmt)

    def mark_success(self, payment: Payment, *, transaction_id: str) -> Payment:

        return self.update(payment, status=PaymentStatus.SUCCESS, transaction_id=transaction_id)

    def mark_failed(self, payment: Payment) -> Payment:

        return self.update(payment, status=PaymentStatus.FAILED)

    def mark_cancelled(self, payment: Payment) -> Payment:

        return self.update(payment, status=PaymentStatus.CANCELLED)

    def total_successful_amount(self, tenant_id: uuid.UUID) -> int:
        stmt = (
            select(func.sum(Payment.amount))
            .where(Payment.tenant_id == tenant_id, Payment.status == PaymentStatus.SUCCESS)
        )

        return self.db.scalar(stmt) or 0

    def count_successful(self, tenant_id: uuid.UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(Payment)
            .where(Payment.tenant_id == tenant_id, Payment.status == PaymentStatus.SUCCESS)
        )

        return self.db.scalar(stmt) or 0

    def exists_reference(self, reference: str) -> bool:
        stmt = select(Payment.id).where(Payment.reference == reference)

        return self.db.scalar(stmt) is not None