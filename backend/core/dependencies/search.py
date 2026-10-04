from __future__ import annotations
from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db
from services.search_service import SearchService

def get_search_service(db: Session = Depends(get_db)) -> SearchService:
    return SearchService(db)
