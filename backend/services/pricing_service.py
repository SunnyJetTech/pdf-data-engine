from __future__ import annotations
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.models import PricingPlan
from schema.pricing_schema import PricingCreate, PricingUpdate

class PricingService:

    @staticmethod
    def all(db: Session) -> list[PricingPlan]:
        return db.query(PricingPlan).order_by(PricingPlan.amount).all()

    @staticmethod
    def public(db: Session) -> list[PricingPlan]:
        return db.query(PricingPlan).filter(PricingPlan.active.is_(True)).order_by(PricingPlan.amount).all()

    @staticmethod
    def get(db: Session, pricing_id: int) -> PricingPlan:

        plan = db.query(PricingPlan).filter(PricingPlan.id == pricing_id).first()

        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pricing plan not found",
            )

        return plan

    @classmethod
    def create(cls, db: Session, payload: PricingCreate) -> PricingPlan:

        existing = db.query(PricingPlan).filter(PricingPlan.name == payload.name).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Pricing plan already exists",
            )

        plan = PricingPlan(**payload.model_dump())

        db.add(plan)
        db.commit()
        db.refresh(plan)

        return plan

    @classmethod
    def update(cls, db: Session, pricing_id: int, payload: PricingUpdate) -> PricingPlan:

        plan = cls.get(db=db, pricing_id=pricing_id)

        updates = payload.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(plan, field, value)

        db.commit()
        db.refresh(plan)

        return plan

    @classmethod
    def delete(cls, db: Session, pricing_id: int,) -> None:

        plan = cls.get(db=db, pricing_id=pricing_id)

        db.delete(plan)
        db.commit()

    @staticmethod
    def serialize(plan: PricingPlan) -> dict:

        return {
            "id": plan.id,
            "name": plan.name,
            "amount": plan.amount,
            "description": plan.description,
            "active": plan.active,
            "created_at": plan.created_at,
        }

    @classmethod
    def serialize_many(cls, plans: list[PricingPlan]) -> list[dict]:

        return [
            cls.serialize(plan)
            for plan in plans
        ]
        
