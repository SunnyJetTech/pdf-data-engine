from __future__ import annotations
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.models.api_key import APIKey
from core.models.user import User
from core.responses_builder import success
from db.database import get_db
from schemas.api_key_schema import APIKeyCreateRequest, APIKeyResponse
from schemas.response_schema import APIResponse
from services.api_key_service import APIKeyService
from services.api_key_usage_service import APIKeyUsageService

router = APIRouter(
    prefix="/api-keys",
    tags=["API Keys"],
)

def _current_tenant_id(current_user: User) -> UUID:
    tenant_id = current_user.current_tenant_id

    if tenant_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not have a current tenant.")

    return tenant_id

def _require_owned_key(*, service: APIKeyService, key_id: UUID, tenant_id: UUID) -> APIKey:
    key = service.by_id(key_id)

    if key.tenant_id != tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this API key.")

    return key

@router.post("", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_api_key(payload: APIKeyCreateRequest, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)

    service = APIKeyService(db)
    key, plaintext = service.create(tenant_id=tenant_id, created_by=current_user.id, name=payload.name, expires_at=payload.expires_at)

    db.commit()
    db.refresh(key)

    return success(
        {
            "key": APIKeyResponse.model_validate(key),
            "plaintext_key": plaintext,
        },
        "API key created successfully. Store the plaintext key securely; it cannot be retrieved again.",
    )


@router.get("", response_model=APIResponse)
def list_api_keys(current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = APIKeyService(db)
    keys = service.by_tenant(tenant_id)

    return success([APIKeyResponse.model_validate(key) for key in keys], "API keys retrieved successfully.")


@router.get("/{key_id}", response_model=APIResponse)
def get_api_key(key_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)

    service = APIKeyService(db)
    key = _require_owned_key( service=service, key_id=key_id, tenant_id=tenant_id)

    return success(APIKeyResponse.model_validate(key), "API key retrieved successfully.")

@router.post("/{key_id}/rotate", response_model=APIResponse)
def rotate_api_key(key_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = APIKeyService(db)

    key = _require_owned_key(service=service, key_id=key_id, tenant_id=tenant_id)
    plaintext = service.rotate(key=key)

    db.commit()
    db.refresh(key)

    return success(
        {
            "key": APIKeyResponse.model_validate(key),
            "plaintext_key": plaintext,
        },
        "API key rotated successfully. Store the new plaintext key securely.",
    )


@router.post("/{key_id}/revoke", response_model=APIResponse)
def revoke_api_key(key_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = APIKeyService(db)

    key = _require_owned_key(service=service, key_id=key_id, tenant_id=tenant_id)
    service.revoke(key)

    db.commit()
    db.refresh(key)

    return success(APIKeyResponse.model_validate(key), "API key revoked successfully.")

@router.post("/{key_id}/activate", response_model=APIResponse)
def activate_api_key(key_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = APIKeyService(db)

    key = _require_owned_key(service=service, key_id=key_id, tenant_id=tenant_id)
    service.activate(key)

    db.commit()
    db.refresh(key)

    return success(APIKeyResponse.model_validate(key), "API key activated successfully.")


@router.delete("/{key_id}", response_model=APIResponse)
def delete_api_key(key_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = APIKeyService(db)
    key = _require_owned_key( service=service, key_id=key_id, tenant_id=tenant_id)
    service.delete(key)

    db.commit()

    return success(message="API key deleted successfully.")

@router.get("/{key_id}/usage", response_model=APIResponse)
def get_api_key_usage(key_id: UUID, limit: int = 100, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)

    service = APIKeyService(db)

    _require_owned_key(service=service, key_id=key_id, tenant_id=tenant_id)

    usage_service = APIKeyUsageService(db)
    usage = usage_service.by_api_key(key_id, limit=limit)

    return success(usage, "API key usage retrieved successfully.")

@router.get("/usage/current-tenant", response_model=APIResponse)
def get_current_tenant_api_key_usage(limit: int = 100, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)

    service = APIKeyUsageService(db)
    usage = service.by_tenant(tenant_id, limit=limit)

    return success(usage, "API key usage retrieved successfully.")