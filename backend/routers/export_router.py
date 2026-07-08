from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from db.database import get_db
from core.auth import get_current_user_from_cookie
from core.models import User
from schema.export_schema import ExportRequest
from services.export_service import ExportService

router = APIRouter(
    prefix="/export",
    tags=["Export"],
)

@router.post("/csv")
def export_csv(payload: ExportRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):

    file, filename = ExportService.export_csv(db=db, user=current_user, payload=payload)

    return StreamingResponse(
        iter([file.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition":
            f'attachment; filename="{filename}"'
        },
    )


@router.post("/excel")
def export_excel(payload: ExportRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):

    file, filename = ExportService.export_excel(db=db, user=current_user, payload=payload)

    return StreamingResponse(
        file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition":
            f'attachment; filename="{filename}"'
        },
    )