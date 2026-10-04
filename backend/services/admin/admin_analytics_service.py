from __future__ import annotations
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from core.models import User, Document, SearchHistory, Payment

class AdminAnalyticsService:
    @staticmethod
    def revenue(db: Session):

        rows = (
            db.query(
                func.date(Payment.created_at).label("date"),
                func.sum(Payment.amount).label("amount"),
            )
            .filter(Payment.status == "success")
            .group_by(func.date(Payment.created_at))
            .order_by(func.date(Payment.created_at))
            .all()
        )

        return [
            {
                "date": row.date,
                "amount": float(row.amount),
            }
            for row in rows
        ]
        
    @staticmethod
    def users(db: Session):

        rows = (
            db.query(
                func.date(User.created_at).label("date"),
                func.count(User.id).label("users"),
            )
            .group_by(func.date(User.created_at))
            .order_by(func.date(User.created_at))
            .all()
        )

        return [
            {
                "date": row.date,
                "users": row.users,
            }
            for row in rows
        ]
        
    @staticmethod
    def uploads(db: Session):

        rows = (
            db.query(
                func.date(Document.created_at).label("date"),
                func.count(Document.id).label("uploads"),
            )
            .group_by(func.date(Document.created_at))
            .order_by(func.date(Document.created_at))
            .all()
        )

        return [
            {
                "date": row.date,
                "uploads": row.uploads,
            }
            for row in rows
        ]
        
    @staticmethod
    def searches(db: Session):

        rows = (
            db.query(
                func.date(SearchHistory.created_at).label("date"),
                func.count(SearchHistory.id).label("searches"),
            )
            .group_by(func.date(SearchHistory.created_at))
            .order_by(func.date(SearchHistory.created_at))
            .all()
        )

        return [
            {
                "date": row.date,
                "searches": row.searches,
            }
            for row in rows
        ]