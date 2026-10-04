from __future__ import annotations
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from core.models import (User, Document, Subscription, Payment, SearchHistory)

class AdminDashboardService:

    @classmethod
    def dashboard(cls, db: Session) -> dict:

        today = datetime.utcnow().date()

        tomorrow = today + timedelta(days=1)

        total_users = db.query(func.count(User.id)).scalar() or 0

        active_users = db.query(func.count(User.id)).filter(User.is_active.is_(True)).scalar() or 0

        total_documents = db.query(func.count(Document.id)).scalar() or 0

        active_subscriptions = db.query(func.count(Subscription.id)).filter(Subscription.is_active.is_(True)).scalar() or 0

        successful_payments = db.query(func.count(Payment.id)).filter(Payment.status == "success").scalar() or 0

        total_revenue = db.query(func.coalesce(func.sum(Payment.amount), 0)).filter(Payment.status == "success").scalar() or 0

        uploads_today = db.query(func.count(Document.id)).filter(Document.created_at >= today, Document.created_at < tomorrow,).scalar() or 0

        searches_today = db.query(func.count(SearchHistory.id)).filter(SearchHistory.created_at >= today, SearchHistory.created_at < tomorrow,).scalar() or 0

        return {
            "total_users": total_users,
            "active_users": active_users,
            "total_documents": total_documents,
            "active_subscriptions": active_subscriptions,
            "successful_payments": successful_payments,
            "total_revenue": float(total_revenue),
            "uploads_today": uploads_today,
            "searches_today": searches_today,
        }