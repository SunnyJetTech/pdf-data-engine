from fastapi import APIRouter, Depends
from schema.user_schema import UserOut, APIResponse, OptionalUserResponse, AdminCheckResponse
from core.functions import (get_current_user_from_cookie, get_optional_user)

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.get("/me", response_model=APIResponse)
def read_current_user(user=Depends(get_current_user_from_cookie)):
    return APIResponse(
        status="success",
        data=UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin,
            has_active_subscription=user.has_active_subscription,
            subscription_date=user.subscription_date,
            subscription_expiry=user.subscription_expiry,
        ).model_dump()
    )

@router.get("/optional-me", response_model=OptionalUserResponse)
def read_optional_user(user=Depends(get_optional_user)):
    if not user:
        return OptionalUserResponse(status="success", message="Guest user", data=None)

    return OptionalUserResponse(
        status="success",
        message="Logged in user",
        data=UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin,
            has_active_subscription=user.has_active_subscription,
            subscription_date=user.subscription_date,
            subscription_expiry=user.subscription_expiry,
        )
    )

@router.get("/admin-check", response_model=AdminCheckResponse)
def admin_check(user=Depends(get_current_user_from_cookie)):
    if not user.is_admin:
        return AdminCheckResponse(status="error", message="Access denied", data=None)

    return AdminCheckResponse(
        status="success",
        message="Admin verified",
        data={
            "user_id": user.id,
            "email": user.email
        }
    )