# new file

from __future__ import annotations
import uuid
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from core.models.api_key import APIKey
from schemas.api_key import APIKeyCreate, APIKeyCreatedResponse, APIKeyResponse,
from services.api_key_service import APIKeyService
from services.authorization_service import AuthorizationService

router = APIRouter(
    prefix="/tenants/{tenant_id}/api-keys",
    tags=["API Keys"],
)

def get_api_key_service(db: Annotated[Session, Depends(get_db)]) -> APIKeyService:
    return APIKeyService(db)


def get_authorization_service(db: Annotated[Session, Depends(get_db)]) -> AuthorizationService:
    return AuthorizationService(db)


@router.post( "", response_model=APIKeyCreatedResponse, status_code=status.HTTP_201_CREATED)
def create_api_key(
    tenant_id: uuid.UUID,
    payload: APIKeyCreate,
    db: Annotated[Session, Depends(get_db)],
    api_key_service: Annotated[APIKeyService, Depends(get_api_key_service)],
    authorization_service: Annotated[AuthorizationService, Depends(get_authorization_service)],
    current_user=Depends(...),
):
    authorization_service.require_permission(current_user, tenant_id, "api_keys:manage")

    api_key, plaintext_key = api_key_service.create(tenant_id=tenant_id, name=payload.name, created_by=current_user.id, expires_at=payload.expires_at)

    return APIKeyCreatedResponse(**api_key.__dict__, plaintext_key=plaintext_key)


@router.get("", response_model=list[APIKeyResponse])
def list_api_keys(
    tenant_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    api_key_service: Annotated[APIKeyService, Depends(get_api_key_service)],
    authorization_service: Annotated[AuthorizationService, Depends(get_authorization_service)],
    current_user=Depends(...),
):
    authorization_service.require_permission(current_user, tenant_id, "api_keys:read")

    return api_key_service.by_tenant(tenant_id)


@router.get("/{key_id}", response_model=APIKeyResponse)
def get_api_key(
    tenant_id: uuid.UUID,
    key_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    api_key_service: Annotated[APIKeyService, Depends(get_api_key_service)],
    authorization_service: Annotated[AuthorizationService, Depends(get_authorization_service)],
    current_user=Depends(...),
):
    authorization_service.require_permission(current_user, tenant_id, "api_keys:read")

    key = api_key_service.by_id(key_id)

    if not key or key.tenant_id != tenant_id:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="API key not found.")

    return key


@router.post("/{key_id}/rotate", response_model=APIKeyCreatedResponse)
def rotate_api_key(
    tenant_id: uuid.UUID,
    key_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    api_key_service: Annotated[ APIKeyService, Depends(get_api_key_service)],
    authorization_service: Annotated[ AuthorizationService, Depends(get_authorization_service)],
    current_user=Depends(...),
):
    authorization_service.require_permission(current_user, tenant_id, "api_keys:manage")

    key = api_key_service.by_id(key_id)

    if not key or key.tenant_id != tenant_id:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="API key not found.")

    key, plaintext_key = api_key_service.rotate(key)

    return APIKeyCreatedResponse(**key.__dict__, plaintext_key=plaintext_key)


@router.post("/{key_id}/revoke", response_model=APIKeyResponse)
def revoke_api_key(
    tenant_id: uuid.UUID,
    key_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    api_key_service: Annotated[ APIKeyService, Depends(get_api_key_service)],
    authorization_service: Annotated[ AuthorizationService, Depends(get_authorization_service)],
    current_user=Depends(...),
):
    authorization_service.require_permission( current_user, tenant_id, "api_keys:manage")

    key = api_key_service.by_id(key_id)

    if not key or key.tenant_id != tenant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found.")

    return api_key_service.revoke(key)


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_api_key(
    tenant_id: uuid.UUID,
    key_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    api_key_service: Annotated[ APIKeyService, Depends(get_api_key_service)],
    authorization_service: Annotated[ AuthorizationService, Depends(get_authorization_service)],
    current_user=Depends(...),
):
    authorization_service.require_permission( current_user, tenant_id, "api_keys:manage")

    key = api_key_service.by_id(key_id)

    if not key or key.tenant_id != tenant_id:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="API key not found.")

    api_key_service.delete(key)