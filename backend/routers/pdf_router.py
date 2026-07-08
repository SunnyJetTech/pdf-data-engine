from fastapi import APIRouter, Depends, File, Form, UploadFile, WebSocket
from sqlalchemy.orm import Session
from db.database import get_db
from core.auth import get_current_user_from_cookie
from core.models.user import User
from core.websocket import manager
from core.constants.file_constants import SaveMode
from schema.response_schema import APIResponse
from services.pdf_service import PDFService

router = APIRouter(
    prefix="/pdf",
    tags=["PDF"],
)

@router.post("/upload", response_model=APIResponse)
async def upload_pdf(
    client_id: str = Form(...),
    file: UploadFile = File(...),
    has_header: bool = Form(True),
    save_mode: SaveMode = Form(SaveMode.DATABASE),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_cookie),
):
    data = await PDFService.upload(
        db=db,
        file=file,
        current_user=current_user,
        client_id=client_id,
        has_header=has_header,
        save_mode=save_mode,
    )

    return APIResponse(
        status="success",
        message="PDF processed successfully.",
        data=data,
    )

@router.websocket("/progress/{client_id}")
async def websocket_progress(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)

    try:
        while True:
            await websocket.receive_text()

    except Exception:
        manager.disconnect(client_id)