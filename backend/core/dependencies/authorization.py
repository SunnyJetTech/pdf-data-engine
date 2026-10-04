from __future__ import annotations
from typing import Callable
from uuid import UUID
from fastapi import Depends
from core.models.user import User
from db.database import get_db
from services.authorization_service import AuthorizationService
from dependencies.auth import get_current_user


def require_permission(resource: str, action: str) -> Callable:
    def dependency(tenant_id: UUID, current_user: User = Depends(get_current_user), db=Depends(get_db)) -> User:
        authorization = AuthorizationService(db)
        authorization.require_permission( user=current_user, tenant_id=tenant_id, resource=resource, action=action)

        return current_user

    return dependency