from sqlalchemy.orm import Session
from core.models import Document, User, Quota
from core.config import settings

class UsageService:
    @staticmethod
    def check_document_limit(db: Session, user: User) -> None:

        total = db.query(Document).filter(Document.user_id == user.id).count()

        quota = db.query(Quota).filter(Quota.user_id == user.id).first()

        limit = (
            quota.uploads_limit
            if quota
            else 3
        )

        if total >= limit:
            raise ValueError("Document upload limit reached.")

    @staticmethod
    def check_file_size(size_bytes: int, max_mb: int | None = None,) -> None:

        limit_mb = max_mb or settings.MAX_FREE_FILE_SIZE_MB

        max_bytes = limit_mb * 1024 * 1024

        if size_bytes > max_bytes:
            raise ValueError(f"Maximum upload size is {limit_mb} MB.")

    @staticmethod
    def check_row_limit(row_count: int, max_rows: int = 50000) -> None:

        if row_count > max_rows:
            raise ValueError(f"Maximum row limit is {max_rows:,}.")

    @staticmethod
    def increment_upload_usage(db: Session, user: User) -> None:

        quota = db.query(Quota).filter(Quota.user_id == user.id).first()

        if quota:
            quota.uploads_used += 1
            db.commit()

    @staticmethod
    def increment_search_usage(db: Session, user: User) -> None:
        quota = db.query(Quota).filter(Quota.user_id == user.id).first()

        if quota:
            quota.searches_used += 1
            db.commit()