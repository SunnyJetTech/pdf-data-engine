from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.auth import admin_required
from core.models import User
from core.responses_builder import success, created
from db.database import get_db
from schema.pricing_schema import PricingCreate, PricingUpdate
from services.admin_service import AdminService
from services.pricing_service import PricingService
from services.quota_service import QuotaService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

@router.get("/users")
def users(db: Session = Depends(get_db), _: User = Depends(admin_required)):
    return success(
        data=AdminService.users(db),
        message="Users retrieved successfully.",
    )

@router.get("/users/{user_id}")
def user(user_id: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    user = AdminService.user(db=db, user_id=user_id,)

    return success(
        data={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
        },
        message="User retrieved successfully.",
    )

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    AdminService.delete_user(db=db, user_id=user_id)

    return success(message="User deleted successfully.")

@router.get("/documents")
def documents( db: Session = Depends(get_db), _: User = Depends(admin_required)):
    return success(
        data=AdminService.documents(db),
        message="Documents retrieved successfully.",
    )

@router.get("/documents/user/{user_id}")
def documents_by_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    return success(
        data=AdminService.documents_by_user(db=db, user_id=user_id),
        message="User documents retrieved successfully.",
    )

@router.delete("/documents/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    AdminService.delete_document(db=db, document_id=document_id,)

    return success(
        message="Document deleted successfully.",
    )

@router.get("/pricing")
def pricing(db: Session = Depends(get_db), _: User = Depends(admin_required)):
    return success(
        data=PricingService.serialize_many(PricingService.all(db)),
        message="Pricing plans retrieved successfully.",
    )

@router.get("/pricing/public")
def public_pricing(db: Session = Depends(get_db)):
    return success(
        data=PricingService.serialize_many(PricingService.public(db)),
        message="Pricing plans retrieved successfully.",
    )

@router.post("/pricing")
def create_pricing(payload: PricingCreate, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    plan = PricingService.create(db=db, payload=payload)

    return created(
        data=PricingService.serialize(plan),
        message="Pricing plan created successfully.",
    )

@router.put("/pricing/{pricing_id}")
def update_pricing(pricing_id: int, payload: PricingUpdate, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    plan = PricingService.update(db=db, pricing_id=pricing_id, payload=payload)

    return success(
        data=PricingService.serialize(plan),
        message="Pricing plan updated successfully.",
    )

@router.delete("/pricing/{pricing_id}")
def delete_pricing(pricing_id: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    PricingService.delete(db=db, pricing_id=pricing_id)

    return success(
        message="Pricing plan deleted successfully.",
    )

@router.get("/quotas")
def quotas(db: Session = Depends(get_db), _: User = Depends(admin_required)):
    return success(
        data=QuotaService.serialize_many(QuotaService.all(db)),
        message="Quotas retrieved successfully.",
    )

@router.get("/quotas/{user_id}")
def quota(user_id: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    quota = QuotaService.get(db=db, user_id=user_id)

    return success(
        data=QuotaService.serialize(quota),
        message="Quota retrieved successfully.",
    )

@router.post("/quotas")
def create_quota(user_id: int, uploads_limit: int, searches_limit: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    quota = QuotaService.create(db=db, user_id=user_id, uploads_limit=uploads_limit, searches_limit=searches_limit)

    return created(
        data=QuotaService.serialize(quota),
        message="Quota created successfully.",
    )

@router.put("/quotas/{user_id}")
def update_quota(user_id: int, uploads_limit: int, searches_limit: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    quota = QuotaService.update(db=db, user_id=user_id, uploads_limit=uploads_limit, searches_limit=searches_limit)

    return success(
        data=QuotaService.serialize(quota),
        message="Quota updated successfully.",
    )

@router.put("/quotas/{user_id}/reset")
def reset_quota(user_id: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    quota = QuotaService.reset_usage(db=db, user_id=user_id)

    return success(
        data=QuotaService.serialize(quota),
        message="Quota reset successfully.",
    )

@router.delete("/quotas/{user_id}")
def delete_quota(user_id: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    QuotaService.delete(db=db, user_id=user_id)

    return success(
        message="Quota deleted successfully.",
    )