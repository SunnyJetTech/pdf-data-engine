from __future__ import annotations
from typing import Any, Generic, TypeVar
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):

    def __init__(self, db: Session, model: type[ModelType]) -> None:
        self.db = db
        self.model = model

    def create(self, **kwargs: Any) -> ModelType:
        instance = self.model(**kwargs)
        self.db.add(instance)
        return instance

    def get(self, object_id: UUID) -> ModelType | None:
        return self.db.get(self.model, object_id)

    def list(self, *, offset: int = 0, limit: int = 100) -> list[ModelType]:

        stmt = select(self.model).offset(offset).limit(limit)

        return list(self.db.scalars(stmt).all())

    def first(self, **filters: Any) -> ModelType | None:

        stmt = select(self.model).filter_by(**filters)

        return self.db.scalar(stmt)

    def exists(self, **filters: Any) -> bool:
        return self.first(**filters) is not None

    def count(self, **filters: Any) -> int:

        stmt = select(func.count()).select_from(self.model).filter_by(**filters)

        return self.db.scalar(stmt) or 0

    def update(self, instance: ModelType, **kwargs: Any) -> ModelType:

        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        return instance

    def delete(self, instance: ModelType) -> None:

        self.db.delete(instance)

    def flush(self) -> None:
        self.db.flush()

    def refresh(self, instance: ModelType) -> None:
        self.db.refresh(instance)
        
    def get_or_404(self, object_id: UUID) -> ModelType:
        instance = self.get(object_id)

        if instance is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.model.__name__} not found.")

        return instance
    
    def all(self) -> list[ModelType]:
        stmt = select(self.model)

        return list(self.db.scalars(stmt).all())
    
    def filter(self, **filters: Any) -> list[ModelType]:
        stmt = select(self.model).filter_by(**filters)

        return list(self.db.scalars(stmt).all())
    
    def paginate(self, *, offset: int = 0, limit: int = 20, **filters: Any) -> list[ModelType]:
        stmt = select(self.model).filter_by(**filters).offset(offset).limit(limit)

        return list(self.db.scalars(stmt).all())
    
    def delete_many(self, instances: list[ModelType]) -> None:
        for instance in instances:
            self.db.delete(instance)
            
    def soft_delete(self, instance: ModelType):
        if hasattr(instance, "deleted_at"):
            instance.deleted_at = datetime.utcnow()
        else:
            self.delete(instance)
            
    def restore(self, instance: ModelType):
        if hasattr(instance, "deleted_at"):
            instance.deleted_at = None
            
    def touch(self, instance: ModelType):
        self.db.add(instance)
        
    def add(self, instance: ModelType) -> ModelType:
        self.db.add(instance)
        return instance