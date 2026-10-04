from __future__ import annotations
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.models.pricing_plan import PricingPlan
from repositories.pricing_plan_repository import PricingPlanRepository

class PricingService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.plans = PricingPlanRepository(db)

    def get(self, plan_id: UUID) -> PricingPlan:
        plan = self.plans.by_id(plan_id)

        if plan is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pricing plan not found.")

        return plan

    def free_plan(self) -> PricingPlan:
        plan = self.plans.free_plan()

        if plan is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Default pricing plan is not configured.")

        return plan

    def active_plans(self) -> list[PricingPlan]:

        return self.plans.active()

    def all(self) -> list[PricingPlan]:

        return self.plans.list()

    def create(self, **data) -> PricingPlan:
        if self.plans.by_name(name=data["name"]):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Pricing plan already exists.")

        self._validate(data)
        plan = PricingPlan(**data)
        self.plans.add(plan)
        self.db.commit()
        self.db.refresh(plan)

        return plan

    def update(self, plan: PricingPlan, **changes) -> PricingPlan:
        self._validate(changes)

        for key, value in changes.items():
            setattr(plan, key, value)

        self.db.commit()
        self.db.refresh(plan)

        return plan

    def activate(self, plan: PricingPlan) -> PricingPlan:
        plan.active = True
        self.db.commit()
        self.db.refresh(plan)

        return plan

    def deactivate(self, plan: PricingPlan) -> PricingPlan:
        plan.active = False
        self.db.commit()
        self.db.refresh(plan)

        return plan

    def delete(self, plan: PricingPlan) -> None:
        self.plans.delete(plan)
        self.db.commit()

    @staticmethod
    def _validate(values: dict) -> None:

        integer_fields = [
            "amount",
            "duration_days",
            "datasets_limit",
            "documents_limit",
            "searches_limit",
            "chat_messages_limit",
            "exports_limit",
            "storage_limit_mb",
            "ai_tokens_limit",
        ]

        for field in integer_fields:
            if field not in values:
                continue

            value = values[field]

            if value is None:
                continue

            if value < 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{field} cannot be negative.")

    @staticmethod
    def serialize(plan: PricingPlan) -> dict:

        return {
            "id": str(plan.id),
            "name": plan.name,
            "description": plan.description,
            "amount": plan.amount,
            "currency": plan.currency,
            "duration_days": plan.duration_days,
            "datasets_limit": plan.datasets_limit,
            "documents_limit": plan.documents_limit,
            "searches_limit": plan.searches_limit,
            "chat_messages_limit": plan.chat_messages_limit,
            "exports_limit": plan.exports_limit,
            "storage_limit_mb": plan.storage_limit_mb,
            "ai_tokens_limit": plan.ai_tokens_limit,
            "active": plan.active,
        }

    @classmethod
    def serialize_many(cls, plans: list[PricingPlan]) -> list[dict]:

        return [cls.serialize(plan) for plan in plans]