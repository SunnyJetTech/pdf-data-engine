from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.models.user import User
from core.responses_builder import success
from db.database import get_db
from schemas.response_schema import APIResponse
from services.subscription.quota_service import QuotaService

router = APIRouter(
    prefix="/quotas",
    tags=["Quotas"],
)

@router.get("/current", response_model=APIResponse)
def get_current_quota( db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    service = QuotaService(db)

    quota = service.get(current_user.current_tenant_id)

    return success(service.serialize(quota), "Quota retrieved successfully.")