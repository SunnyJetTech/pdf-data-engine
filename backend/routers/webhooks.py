from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from core.auth import get_current_user_from_cookie
from core.models.user import User
from core.responses_builder import success
from db.database import get_db
from repositories.webhook_repository import WebhookRepository
from schemas.response_schema import APIResponse
from schemas.webhook_schema import WebhookCreate, WebhookCreatedResponse, WebhookResponse, WebhookSecretRotationResponse, WebhookUpdate
from services.webhook_delivery_service import WebhookDeliveryService
from services.webhook_service import WebhookService

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
)

def _current_tenant_id(current_user: User) -> UUID:
    tenant_id = current_user.current_tenant_id

    if tenant_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not have a current tenant.")

    return tenant_id

def _owned_webhook(*, service: WebhookService, webhook_id: UUID, tenant_id: UUID):
    webhook = service.by_id(webhook_id)

    if webhook.tenant_id != tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this webhook.")

    return webhook

@router.post("", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_webhook(payload: WebhookCreate, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = WebhookService(db)

    webhook, secret = service.create(
        tenant_id=tenant_id,
        name=payload.name,
        url=payload.url,
        events=payload.events,
        description=payload.description,
        retry_count=payload.retry_count,
        timeout_seconds=payload.timeout_seconds,
    )

    db.commit()
    db.refresh(webhook)

    data = WebhookCreatedResponse(**WebhookResponse.model_validate(webhook).model_dump(), secret=secret)

    return success(data, "Webhook created successfully. Store the secret securely; it cannot be retrieved again.")

@router.get("", response_model=APIResponse)
def list_webhooks(current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = WebhookService(db)
    webhooks = service.by_tenant(tenant_id)

    return success([WebhookResponse.model_validate(webhook) for webhook in webhooks],  "Webhooks retrieved successfully.")

@router.get("/{webhook_id}/deliveries", response_model=APIResponse)
def webhook_delivery_history(
    webhook_id: UUID,
    limit: int = Query(default=100, ge=1, le=1000),
    current_user: User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db),
):
    tenant_id = _current_tenant_id(current_user)
    webhook_service = WebhookService(db)

    _owned_webhook(service=webhook_service, webhook_id=webhook_id, tenant_id=tenant_id)

    delivery_service = WebhookDeliveryService(db)
    deliveries = delivery_service.history(webhook_id, limit=limit)

    return success(deliveries, "Webhook delivery history retrieved successfully.")


@router.get("/{webhook_id}/deliveries/latest", response_model=APIResponse)
def latest_webhook_delivery(webhook_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    webhook_service = WebhookService(db)

    _owned_webhook(service=webhook_service, webhook_id=webhook_id, tenant_id=tenant_id)

    delivery_service = WebhookDeliveryService(db)
    delivery = delivery_service.latest(webhook_id)

    return success( delivery, "Latest webhook delivery retrieved successfully.")


@router.get("/{webhook_id}/deliveries/failed", response_model=APIResponse)
def failed_webhook_deliveries(webhook_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)

    webhook_service = WebhookService(db)

    _owned_webhook( service=webhook_service, webhook_id=webhook_id, tenant_id=tenant_id)

    delivery_service = WebhookDeliveryService(db)
    deliveries = delivery_service.failed(webhook_id)

    return success(deliveries, "Failed webhook deliveries retrieved successfully.")

@router.get("/{webhook_id}/deliveries/successful", response_model=APIResponse)
def successful_webhook_deliveries(webhook_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)

    webhook_service = WebhookService(db)

    _owned_webhook(service=webhook_service, webhook_id=webhook_id, tenant_id=tenant_id)

    delivery_service = WebhookDeliveryService(db)
    deliveries = delivery_service.successful(webhook_id)

    return success(deliveries, "Successful webhook deliveries retrieved successfully.")

@router.get("/{webhook_id}", response_model=APIResponse)
def get_webhook(webhook_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)

    service = WebhookService(db)
    webhook = _owned_webhook(service=service, webhook_id=webhook_id, tenant_id=tenant_id)

    return success(WebhookResponse.model_validate(webhook), "Webhook retrieved successfully.")

@router.patch("/{webhook_id}", response_model=APIResponse)
def update_webhook(webhook_id: UUID, payload: WebhookUpdate, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = WebhookService(db)

    webhook = _owned_webhook( service=service, webhook_id=webhook_id, tenant_id=tenant_id)
    webhook = service.update(
        webhook=webhook,
        name=payload.name,
        url=payload.url,
        events=payload.events,
        description=payload.description,
        retry_count=payload.retry_count,
        timeout_seconds=payload.timeout_seconds,
    )

    db.commit()
    db.refresh(webhook)

    return success(WebhookResponse.model_validate(webhook), "Webhook updated successfully.")

@router.post("/{webhook_id}/rotate-secret", response_model=APIResponse)
def rotate_webhook_secret(webhook_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)

    service = WebhookService(db)
    webhook = _owned_webhook(service=service, webhook_id=webhook_id, tenant_id=tenant_id)
    webhook, secret = service.rotate_secret(webhook)

    db.commit()
    db.refresh(webhook)

    data = WebhookSecretRotationResponse(**WebhookResponse.model_validate(webhook).model_dump(), secret=secret)

    return success(data, "Webhook secret rotated successfully. Store the new secret securely.")

@router.post( "/{webhook_id}/activate", response_model=APIResponse)
def activate_webhook( webhook_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = WebhookService(db)

    webhook = _owned_webhook( service=service, webhook_id=webhook_id, tenant_id=tenant_id)
    service.activate(webhook)

    db.commit()
    db.refresh(webhook)

    return success( WebhookResponse.model_validate(webhook), "Webhook activated successfully.")

@router.post("/{webhook_id}/deactivate", response_model=APIResponse)
def deactivate_webhook(webhook_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = WebhookService(db)

    webhook = _owned_webhook( service=service, webhook_id=webhook_id, tenant_id=tenant_id)
    service.deactivate(webhook)

    db.commit()
    db.refresh(webhook)

    return success(WebhookResponse.model_validate(webhook), "Webhook deactivated successfully.")

@router.delete("/{webhook_id}", response_model=APIResponse)
def delete_webhook(webhook_id: UUID, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    tenant_id = _current_tenant_id(current_user)
    service = WebhookService(db)

    webhook = _owned_webhook(service=service, webhook_id=webhook_id, tenant_id=tenant_id)
    service.delete(webhook)

    db.commit()

    return success(message="Webhook deleted successfully.")