from __future__ import annotations
from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db
from services.dataset_service import DatasetService
from services.document_service import DocumentService
from services.ingestion.document_ingestion_service import DocumentIngestionService
from services.upload.upload_service import UploadService

def get_upload_service(db: Session = Depends(get_db)) -> UploadService:

    return UploadService(
        dataset_service=DatasetService(db),
        document_service=DocumentService(db),
        ingestion_service=DocumentIngestionService(db),
    )
