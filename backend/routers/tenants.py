from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.models.user import User
from core.responses_builder import success
from db.database import get_db
from schemas.response_schema import APIResponse
from services.tenant_service import TenantService

router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"],
)

def _current_tenant(*, current_user: User, db: Session):
    tenant_id = current_user.current_tenant_id

    if tenant_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not have a current tenant.")

    service = TenantService(db)

    return service.by_id(tenant_id)

@router.get("/current", response_model=APIResponse)
def get_current_tenant(current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant = _current_tenant(current_user=current_user, db=db)

    return success(tenant, "Current tenant retrieved successfully.")

@router.get("/current/members", response_model=APIResponse)
def get_current_tenant_members(current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant = _current_tenant(current_user=current_user, db=db)
    service = TenantService(db)

    return success(service.members(tenant.id), "Tenant members retrieved successfully.")

@router.get("/current/member-count", response_model=APIResponse)
def get_current_tenant_member_count(current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant = _current_tenant(current_user=current_user, db=db)
    service = TenantService(db)

    return success(service.member_count(tenant.id), "Tenant member count retrieved successfully.")

@router.get("/{tenant_id}", response_model=APIResponse)
def get_tenant(tenant_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    if current_user.current_tenant_id != tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this tenant.")

    service = TenantService(db)
    tenant = service.by_id(tenant_id)

    return success(tenant, "Tenant retrieved successfully.")