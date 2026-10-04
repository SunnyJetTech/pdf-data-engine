from __future__ import annotations
from pandas import DataFrame
from sqlalchemy.orm import Session
from integrations.mongodb import MongoIntegration
from services.document_service import DocumentService

class ExportRepository:

    @staticmethod
    def dataframe(*, db: Session, user_id: int, document_id: int,) -> DataFrame:

        document = DocumentService.get_document(db=db, user_id=user_id, document_id=document_id)

        return MongoIntegration.export(
            collection_name=document.mongo_collection,
        )