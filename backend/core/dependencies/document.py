from __future__ import annotations
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db
from services.document_service import DocumentService

def get_document_service(db: Annotated[Session, Depends(get_db)]) -> DocumentService:
    return DocumentService(db)
