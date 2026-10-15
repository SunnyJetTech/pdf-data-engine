from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.models.user import User
from core.responses_builder import success
from db.database import get_db
from repositories.tenant_member_repository import TenantMemberRepository
from schemas.response_schema import APIResponse

router = APIRouter(
    prefix="/tenant-members",
    tags=["Tenant Members"],
)

def _require_current_tenant(*, current_user: User) -> UUID:
    tenant_id = current_user.current_tenant_id

    if tenant_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not have a current tenant.")

    return tenant_id


@router.get("/me", response_model=APIResponse)
def get_my_membership(current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _require_current_tenant(current_user=current_user)
    repository = TenantMemberRepository(db)

    membership = repository.membership(tenant_id=tenant_id, user_id=current_user.id)

    if membership is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant membership not found.")

    return success(membership, "Tenant membership retrieved successfully.")


@router.get("", response_model=APIResponse)
def list_tenant_members(current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _require_current_tenant(current_user=current_user)
    repository = TenantMemberRepository(db)
    members = repository.tenant_members(tenant_id)

    return success(members, "Tenant members retrieved successfully.")


@router.get("/{member_id}", response_model=APIResponse)
def get_tenant_member(member_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):  
    tenant_id = _require_current_tenant(current_user=current_user)
    repository = TenantMemberRepository(db)
    membership = repository.by_id(member_id)

    if membership is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Tenant membership not found.")

    if membership.tenant_id != tenant_id:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this tenant membership.")

    return success(membership, "Tenant membership retrieved successfully.")