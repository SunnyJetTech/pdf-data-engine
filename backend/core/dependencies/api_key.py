from __future__ import annotations
from typing import Annotated
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from core.models.api_key import APIKey
from db.database import get_db
from services.api_key_service import APIKeyService

def get_api_key_service(db: Annotated[Session, Depends(get_db)]) -> APIKeyService:
    return APIKeyService(db)


async def get_current_api_key(
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
    service: Annotated[APIKeyService, Depends(get_api_key_service)] = None,
) -> APIKey:
    if not x_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key is required.")

    try:
        return service.authenticate(x_api_key)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key.")