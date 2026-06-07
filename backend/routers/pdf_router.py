from fastapi import APIRouter, File, UploadFile, Form, Depends, WebSocket
from sqlalchemy.orm import Session
from db.database import get_db
from schema.file_schema import APIResponse, SaveMode
from core.Models import User, Document
from core.websocket_manager import manager
from core.functions import (
    extract_pdf_table,
    save_to_excel,
    save_to_mongodb,
    get_current_user_from_cookie
)

router = APIRouter(
    prefix="/pdf",
    tags=["PDF"]
)


@router.post("/upload", response_model=APIResponse)
async def upload_pdf(
    client_id: str = Form(...),
    file: UploadFile = File(...),
    has_header: bool = Form(True),
    save_mode: SaveMode = Form(SaveMode.DATABASE),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_cookie)
):
    if file.content_type != "application/pdf":
        return APIResponse(
            status="failed",
            message="Unsupported file format"
        )

    try:
        df = await extract_pdf_table(
            pdf_source=file.file,
            progress_callback=lambda current_page, total_pages:
                manager.send_progress(
                    client_id,
                    current_page,
                    total_pages
                )
        )

        await manager.send_message(
            client_id,
            {
                "status": "processing_complete",
                "rows": len(df),
                "columns": len(df.columns)
            }
        )

        if save_mode == SaveMode.EXCEL:

            excel_file = (file.filename.replace(".pdf", "") + ".xlsx")
            save_to_excel(df=df,excel_file=excel_file)

            await manager.send_message(
                client_id,
                {
                    "status": "saved_to_excel",
                    "file": excel_file
                }
            )

            return APIResponse(
                status="success",
                message="Saved to Excel successfully",
                data={
                    "rows": len(df),
                    "columns": len(df.columns),
                    "file": excel_file
                }
            )

        if save_mode == SaveMode.DATABASE:

            collection_name = (file.filename.replace(".pdf", "").replace(" ", "_").replace("-", "_").lower())
            save_to_mongodb(df=df,collection_name=collection_name)

            document = Document(
                user_id=current_user.id,
                filename=file.filename,
                mongo_collection=collection_name,
                rows_count=len(df),
                columns_count=len(df.columns)
            )

            db.add(document)
            db.commit()
            db.refresh(document)

            await manager.send_message(
                client_id,
                {
                    "status": "saved_to_mongodb",
                    "collection": collection_name
                }
            )

            return APIResponse(
                status="success",
                message="Saved to MongoDB successfully",
                data={
                    "document_id": document.id,
                    "filename": file.filename,
                    "mongo_collection": collection_name,
                    "rows": len(df),
                    "columns": len(df.columns)
                }
            )

        return APIResponse(
            status="success",
            message="File processed successfully",
            data={
                "rows": len(df),
                "columns": len(df.columns)
            }
        )

    except Exception as e:
        await manager.send_message(
            client_id,
            {
                "status": "error",
                "message": str(e)
            }
        )

        return APIResponse(
            status="failed",
            message=str(e)
        )


@router.websocket("/progress/{client_id}")
async def websocket_progress(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)

    try:
        while True:
            await websocket.receive_text()

    except Exception:
        manager.disconnect(client_id)