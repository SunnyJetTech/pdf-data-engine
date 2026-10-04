from __future__ import annotations
from sqlalchemy.orm import Session
from repositories.activity_repository import ActivityRepository
from repositories.dataset_repository import DatasetRepository
from repositories.document_repository import DocumentRepository
from repositories.search_repository import SearchRepository

class UnitOfWork:
    def __init__(self, db: Session):
        self.db = db

        self.datasets = DatasetRepository(db)
        self.documents = DocumentRepository(db)
        self.activities = ActivityRepository(db)
        self.searches = SearchRepository(db)

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def flush(self) -> None:
        self.db.flush()

    def refresh(self, instance) -> None:
        self.db.refresh(instance)

    def close(self) -> None:
        self.db.close()
        