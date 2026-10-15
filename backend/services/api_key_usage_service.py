from __future__ import annotations
import uuid
from sqlalchemy.orm import Session
from core.models.api_key_usage import APIKeyUsage
from repositories.api_key_usage_repository import APIKeyUsageRepository

class APIKeyUsageService:

    def __init__(self, db: Session) -> None:
        self.db = db
        self.usage = APIKeyUsageRepository(db)

    def record(
        self,
        *,
        api_key_id: uuid.UUID,
        tenant_id: uuid.UUID,
        endpoint: str,
        http_method: str,
        status_code: int,
        request_id: str | None = None,
        response_time_ms: int | None = None,
        request_bytes: int | None = None,
        response_bytes: int | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> APIKeyUsage:
        entry = APIKeyUsage(
            api_key_id=api_key_id,
            tenant_id=tenant_id,
            request_id=request_id,
            endpoint=endpoint,
            http_method=http_method,
            status_code=status_code,
            response_time_ms=response_time_ms,
            request_bytes=request_bytes,
            response_bytes=response_bytes,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        self.usage.add(entry)
        self.db.flush()

        return entry

    def by_api_key( self, api_key_id: uuid.UUID, *, limit: int = 100) -> list[APIKeyUsage]:
        return self.usage.by_api_key( api_key_id, limit=limit)

    def by_tenant(self, tenant_id: uuid.UUID, *, limit: int = 100) -> list[APIKeyUsage]:
        return self.usage.by_tenant( tenant_id, limit=limit)