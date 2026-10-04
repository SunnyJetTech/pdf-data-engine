from __future__ import annotations
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from core.models.subscription import PricingPlan
from repositories.base_repository import BaseRepository

class PricingPlanRepository(BaseRepository[PricingPlan]):

    def __init__(self, db: Session):
        super().__init__(db=db, model=PricingPlan)

    def by_id(self, plan_id: int) -> PricingPlan | None:
        stmt = select(PricingPlan).where(PricingPlan.id == plan_id)

        return self.db.scalar(stmt)

    def by_name(self, name: str) -> PricingPlan | None:
        stmt = select(PricingPlan).where(PricingPlan.name == name)

        return self.db.scalar(stmt)

    def active(self) -> list[PricingPlan]:
        stmt = select(PricingPlan).where(PricingPlan.active.is_(True)).order_by(PricingPlan.amount.asc())

        return list(self.db.scalars(stmt).all())

    def inactive(self) -> list[PricingPlan]:
        stmt = select(PricingPlan).where(PricingPlan.active.is_(False)).order_by(PricingPlan.amount.asc())

        return list(self.db.scalars(stmt).all())

    def exists_name(self, name: str) -> bool:
        stmt = select(PricingPlan.id).where(PricingPlan.name == name)

        return self.db.scalar(stmt) is not None

    def activate(self, plan: PricingPlan) -> PricingPlan:
        return self.update(plan, active=True)

    def deactivate(self, plan: PricingPlan) -> PricingPlan:

        return self.update(plan, active=False)

    def count_active(self) -> int:
        stmt = select(func.count()).select_from(PricingPlan).where(PricingPlan.active.is_(True))

        return self.db.scalar(stmt) or 0

    def cheapest(self) -> PricingPlan | None:
        stmt = select(PricingPlan).where(PricingPlan.active.is_(True)).order_by(PricingPlan.amount.asc()).limit(1)

        return self.db.scalar(stmt)

    def most_expensive(self) -> PricingPlan | None:
        stmt = select(PricingPlan).where(PricingPlan.active.is_(True)).order_by(PricingPlan.amount.desc()).limit(1)

        return self.db.scalar(stmt)
    
    def default(self) -> PricingPlan | None:
        stmt = select(PricingPlan).where(PricingPlan.active.is_(True), PricingPlan.is_default.is_(True),).limit(1)

        return self.db.scalar(stmt)