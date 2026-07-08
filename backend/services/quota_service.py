from __future__ import annotations
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.models import Quota
from services.subscription_service import SubscriptionService

class QuotaService:

    @staticmethod
    def all(db: Session) -> list[Quota]:
        return db.query(Quota).order_by(Quota.user_id).all()

    @staticmethod 
    def get(db: Session, user_id: int) -> Quota:

        quota = db.query(Quota).filter(Quota.user_id == user_id).first()

        if not quota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quota not found",
            )

        return quota

    @classmethod
    def create(cls, db: Session, user_id: int, uploads_limit: int, searches_limit: int) -> Quota:

        existing = db.query(Quota).filter(Quota.user_id == user_id).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Quota already exists",
            )

        quota = Quota(
            user_id=user_id,
            uploads_limit=uploads_limit,
            searches_limit=searches_limit,
            uploads_used=0,
            searches_used=0,
        )

        db.add(quota)
        db.commit()
        db.refresh(quota)

        return quota

    @classmethod
    def update(cls, db: Session, user_id: int, uploads_limit: int, searches_limit: int,) -> Quota:

        quota = cls.get(db=db, user_id=user_id)

        quota.uploads_limit = uploads_limit
        quota.searches_limit = searches_limit

        db.commit()
        db.refresh(quota)

        return quota

    @classmethod
    def reset_usage(cls, db: Session, user_id: int,) -> Quota:

        quota = cls.get(db=db, user_id=user_id)

        quota.uploads_used = 0
        quota.searches_used = 0

        db.commit()
        db.refresh(quota)

        return quota

    @classmethod
    def delete(cls, db: Session, user_id: int) -> None:

        quota = cls.get(db=db, user_id=user_id)

        db.delete(quota)
        db.commit()

    @staticmethod
    def serialize(quota: Quota) -> dict:

        return {
            "user_id": quota.user_id,
            "uploads_used": quota.uploads_used,
            "uploads_limit": quota.uploads_limit,
            "searches_used": quota.searches_used,
            "searches_limit": quota.searches_limit,
        }

    @classmethod
    def serialize_many(cls, quotas: list[Quota]) -> list[dict]:

        return [
            cls.serialize(quota)
            for quota in quotas
        ]
        
    @classmethod
    def current(cls, db: Session, user_id: int) -> dict:
        quota = db.query(Quota).filter(
            Quota.user_id == user_id
        ).first()

        if quota:
            return cls.serialize(quota)

        if SubscriptionService.has_active(
            db=db,
            user_id=user_id,
        ):
            return {
                "uploads_used": 0,
                "uploads_limit": 1000,
                "searches_used": 0,
                "searches_limit": 10000,
            }

        return {
            "uploads_used": 0,
            "uploads_limit": 20,
            "searches_used": 0,
            "searches_limit": 50,
        }