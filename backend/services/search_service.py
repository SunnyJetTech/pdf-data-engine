from sqlalchemy.orm import Session
from core.models import SearchHistory
from core.search.query_builder import build_query
from services.document_service import DocumentService

class SearchService:

    @classmethod
    def search(cls, *, db: Session, user_id: int, payload) -> dict:

        document = DocumentService.get_document(db=db, user_id=user_id, document_id=payload.document_id)

        collection = DocumentService.get_collection(document)

        query = build_query(payload.column, payload.operator, payload.value)

        total = collection.count_documents(query)

        skip = (payload.page - 1) * payload.page_size

        rows = list(
            collection.find(
                query,
                {"_id": 0},
            )
            .skip(skip)
            .limit(payload.page_size)
        )

        cls.save_history(db=db,user_id=user_id,document_id=document.id,column=payload.column,operator=payload.operator,value=payload.value)

        return {
            "total": total,
            "page": payload.page,
            "page_size": payload.page_size,
            "results": rows,
        }

    @staticmethod
    def save_history(*, db: Session, user_id: int, document_id: int, column: str, operator: str, value: str) -> SearchHistory:

        history = SearchHistory(user_id=user_id, document_id=document_id, column_name=column, operator=operator, search_value=value)

        db.add(history)
        db.commit()
        db.refresh(history)

        return history

    @staticmethod
    def get_history(*, db: Session, user_id: int, limit: int = 20) -> list[SearchHistory]:

        return (
            db.query(SearchHistory)
            .filter(SearchHistory.user_id == user_id)
            .order_by(SearchHistory.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def serialize_history(history: SearchHistory) -> dict:

        return {
            "id": history.id,
            "document_id": history.document_id,
            "column_name": history.column_name,
            "operator": history.operator,
            "search_value": history.search_value,
            "created_at": history.created_at,
        }

    @classmethod
    def serialize_history_many(cls, histories: list[SearchHistory]) -> list[dict]:

        return [
            cls.serialize_history(item)
            for item in histories
        ]