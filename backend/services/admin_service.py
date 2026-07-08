from __future__ import annotations
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.models import User
from core.models.document import Document
from services.document_service import DocumentService

class AdminService:

    @staticmethod
    def users(db: Session) -> list[dict]:
        users = db.query(User) .order_by(User.id) .all()

        return [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "is_admin": user.is_admin,
            }
            for user in users
        ]

    @staticmethod
    def user(db: Session, user_id: int) -> User:

        user = db.query(User) .filter(User.id == user_id) .first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    @classmethod
    def delete_user(cls, db: Session, user_id: int):

        user = cls.user(db=db, user_id=user_id)

        db.delete(user)
        db.commit()

    @classmethod
    def update_user(cls, db: Session, user_id: int, payload):

        user = cls.user(db=db, user_id=user_id)

        updates = payload.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)

        return user


    @staticmethod
    def documents(db: Session):

        documents = db.query(Document).order_by(Document.created_at.desc()).all()

        return DocumentService.serialize_many(documents)

    @staticmethod
    def documents_by_user(db: Session,user_id: int):

        documents = db.query(Document).filter(Document.user_id == user_id).order_by(Document.created_at.desc()).all()

        return DocumentService.serialize_many(documents)

    @staticmethod
    def delete_document(db: Session,document_id: int):

        document = db.query(Document).filter(Document.id == document_id).first()

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found",
            )

        DocumentService.delete(
            db=db,
            document=document,
        )