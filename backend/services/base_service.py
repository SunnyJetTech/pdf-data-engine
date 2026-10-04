from __future__ import annotations
from sqlalchemy.orm import Session
from services.activity_service import ActivityService

class BaseService:

    def __init__(self, db: Session) -> None:
        self.db = db

        self.activity = ActivityService(db)

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def flush(self) -> None:
        self.db.flush()

    def refresh(self, instance) -> None:
        self.db.refresh(instance)
        
    def commit_refresh(self, instance):

        self.db.commit()
        self.db.refresh(instance)

        return instance
    
    def save(self, repository, instance):
        repository.add(instance)

        return self.commit_refresh(instance)