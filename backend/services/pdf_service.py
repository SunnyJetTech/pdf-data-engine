from fastapi import UploadFile
from sqlalchemy.orm import Session
from core.constants.file_constants import SaveMode
from core.models import User
from core.validators import validate_file_size
from core.websocket import manager
from core.utils.pdf import extract_pdf_table
from services.dataset_service import DatasetService
from backend.services.search.export_service import ExportService
from services.usage_service import UsageService

class PDFService:

    @staticmethod
    async def upload(
        *,
        db: Session,
        file: UploadFile,
        current_user: User,
        client_id: str,
        has_header: bool,
        save_mode: SaveMode,
        dataset_id: int | None = None,
        dataset_name: str | None = None,
    ):

        PDFService._validate_file(file)

        UsageService.check_document_limit(db=db, user=current_user)

        await validate_file_size(file=file, max_size_mb=20)

        dataframe = await extract_pdf_table(
            pdf_source=file.file,
            has_header=has_header,
            progress_callback=lambda current, total: manager.send_progress(
                client_id,
                current,
                total,
            ),
        )

        UsageService.check_row_limit(len(dataframe))

        await manager.send(
            client_id,
            {
                "status": "processing_complete",
                "rows": len(dataframe),
                "columns": len(dataframe.columns),
            },
        )

        if save_mode == SaveMode.EXCEL:

            return await ExportService.export_excel(dataframe=dataframe, filename=file.filename, client_id=client_id)

        if save_mode == SaveMode.DATABASE:

            return await DatasetService.upload(
                db=db,
                dataframe=dataframe,
                filename=file.filename,
                current_user=current_user,
                client_id=client_id,
                dataset_id=dataset_id,
                dataset_name=dataset_name,
            )

        return {
            "rows": len(dataframe),
            "columns": len(dataframe.columns),
        }

    @staticmethod
    def _validate_file(file: UploadFile):

        if file.content_type != "application/pdf":
            raise ValueError("Unsupported file format.")