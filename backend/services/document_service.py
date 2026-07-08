from __future__ import annotations
from typing import Any
from pymongo.collection import Collection
from sqlalchemy.orm import Session
from db.mongo_db import mongodb
from core.models.document import Document
from core.exceptions import DocumentNotFound


class DocumentService:

    @staticmethod
    def get_document(*, db: Session, user_id: int, document_id: int) -> Document:

        document = db.query(Document).filter(Document.id == document_id, Document.user_id == user_id).first()

        if not document:
            raise DocumentNotFound()

        return document

    @staticmethod
    def get_user_documents(*, db: Session, user_id: int) -> list[Document]:

        return db.query(Document).filter(Document.user_id == user_id).order_by(Document.created_at.desc()).all()

    @staticmethod
    def get_collection(document: Document) -> Collection:

        return mongodb[document.mongo_collection]

    @classmethod
    def get_columns(cls, *, db: Session, user_id: int, document_id: int) -> list[str]:

        document = cls.get_document(db=db, user_id=user_id, document_id=document_id)

        collection = cls.get_collection(document)

        first_row = collection.find_one({}, {"_id": 0})

        if not first_row:
            return []

        return list(first_row.keys())
    
    @classmethod
    def get_sample(cls, *, db: Session, user_id: int, document_id: int) -> dict[str, Any]:

        document = cls.get_document(db=db, user_id=user_id, document_id=document_id)

        collection = cls.get_collection(document)

        return collection.find_one({}, {"_id": 0}) or {}
    
    @classmethod
    def get_statistics(cls, *, db: Session, user_id: int, document_id: int) -> dict[str, Any]:

        document = cls.get_document(db=db, user_id=user_id, document_id=document_id)

        collection = cls.get_collection(document)

        return {
            "rows": collection.count_documents({}),
            "columns": document.columns_count,
            "uploaded": document.created_at,
        }

    @staticmethod
    def delete(*, db: Session, document: Document) -> None:

        mongodb.drop_collection(document.mongo_collection)

        db.delete(document)
        db.commit()

    @staticmethod
    def serialize(document: Document) -> dict[str, Any]:

        return {
            "id": document.id,
            "filename": document.filename,
            "mongo_collection": document.mongo_collection,
            "rows": document.rows_count,
            "columns": document.columns_count,
            "created_at": document.created_at,
        }

    @classmethod
    def serialize_many(cls, documents: list[Document]) -> list[dict[str, Any]]:

        return [
            cls.serialize(document)
            for document in documents
        ]