from fastapi import UploadFile
from sqlalchemy.orm import Session
from core.models import User, Document
from core.naming import generate_collection_name
from core.utils.dataframe import save_to_excel
from core.utils.mongodb import save_to_mongodb
from core.utils.pdf import extract_pdf_table
from core.validators import validate_file_size
from core.websocket import manager
from services.document_service import DocumentService
from services.usage_service import UsageService

class PDFService:

    @staticmethod
    async def upload(*,db: Session, file: UploadFile, current_user: User,client_id: str, has_header: bool, save_mode):

        if file.content_type != "application/pdf":
            raise ValueError("Unsupported file format.")

        UsageService.check_document_limit(db=db, user=current_user)

        await validate_file_size(file=file, max_size_mb=20)

        df = await extract_pdf_table(
            pdf_source=file.file,
            has_header=has_header,
            progress_callback=lambda current, total:
                manager.send_progress(
                    client_id,
                    current,
                    total,
                ),
        )

        UsageService.check_row_limit(
            len(df)
        )

        await manager.send(
            client_id,
            {
                "status": "processing_complete",
                "rows": len(df),
                "columns": len(df.columns),
            },
        )

        if save_mode.value == "excel":
            return await PDFService._save_excel(
                df=df,
                file=file,
                client_id=client_id,
            )

        if save_mode.value == "database":
            return await PDFService._save_database(
                db=db,
                df=df,
                file=file,
                current_user=current_user,
                client_id=client_id,
            )

        return {
            "rows": len(df),
            "columns": len(df.columns),
        }

    @staticmethod
    async def _save_excel(
        *,
        df,
        file: UploadFile,
        client_id: str,
    ):
        excel_name = (
            file.filename.replace(".pdf", ".xlsx")
        )

        save_to_excel(
            df=df,
            excel_file=excel_name,
        )

        await manager.send(
            client_id,
            {
                "status": "saved_to_excel",
                "file": excel_name,
            },
        )

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "file": excel_name,
        }

    @staticmethod
    async def _save_database(*, db: Session, df, file: UploadFile, current_user: User, client_id: str,):
        collection_name = generate_collection_name(file.filename)

        save_to_mongodb(dataframe=df, collection_name=collection_name)

        document = Document(user_id=current_user.id, filename=file.filename, mongo_collection=collection_name, rows_count=len(df), columns_count=len(df.columns))

        db.add(document)
        db.commit()
        db.refresh(document)

        UsageService.increment_upload_usage(db=db, user=current_user)

        await manager.send(client_id,
            {
                "status": "saved_to_database",
                "collection": collection_name,
            },
        )

        return DocumentService.serialize(document)