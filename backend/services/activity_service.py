from typing import Optional
from sqlalchemy.orm import Session
from core.constants.activity import ActivityAction
from core.models import Activity

class ActivityService:

    @staticmethod
    def log(*, db: Session, user_id: int, action: str, document_id: Optional[int] = None) -> Activity:
        activity = Activity(user_id=user_id, action=action, document_id=document_id)

        db.add(activity)
        db.commit()
        db.refresh(activity)

        return activity

    @staticmethod
    def get_user_logs(*, db: Session, user_id: int, limit: int = 50) -> list[Activity]:
        return db.query(Activity).filter(Activity.user_id == user_id).order_by(Activity.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_document_logs(*, db: Session, document_id: int) -> list[Activity]:

        return db.query(Activity).filter(Activity.document_id == document_id).order_by(Activity.created_at.desc()).all()

    @staticmethod
    def get_all_logs(*, db: Session, limit: int = 100) -> list[Activity]:
        return db.query(Activity).order_by(Activity.created_at.desc()).limit(limit).all()

    @staticmethod
    def delete_old_logs(*, db: Session, before_date) -> int:
        deleted = db.query(Activity).filter(Activity.created_at < before_date).delete()

        db.commit()

        return deleted