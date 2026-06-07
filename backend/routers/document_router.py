from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from core.Models import User, Document
from core.functions import get_current_user_from_cookie
from db.mongo_db import mongodb
from schema.file_schema import APIResponse
from bson.regex import Regex
from schema.file_schema import APIResponse
from schema.search_schema import SearchDocumentRequest

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.get("/", response_model=APIResponse)
def get_user_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    documents = (db.query(Document).filter(Document.user_id == current_user.id).order_by(Document.created_at.desc()).all())
    
    if not documents:
        return APIResponse(
            status='failed',
            message='No document found'
        )

    return APIResponse(
        status="success",
        message="Documents retrieved",
        data=[
            {
                "id": doc.id,
                "filename": doc.filename,
                "mongo_collection": doc.mongo_collection,
                "rows": doc.rows_count,
                "columns": doc.columns_count,
                "created_at": doc.created_at
            }
            for doc in documents
        ]
    )


@router.delete("/{document_id}", response_model=APIResponse)
def delete_document(document_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    document = (db.query(Document).filter(Document.id == document_id, Document.user_id == current_user.id).first())

    if not document:
        return APIResponse(
            status="failed",
            message="Document not found"
        )

    mongodb.drop_collection(document.mongo_collection)

    db.delete(document)
    db.commit()

    return APIResponse(
        status="success",
        message="Document deleted successfully"
    )

@router.post("/search", response_model=APIResponse)
def search_document(payload: SearchDocumentRequest, db: Session = Depends(get_db),current_user: User = Depends(get_current_user_from_cookie)):
    document = (db.query(Document).filter(Document.id == payload.document_id ,Document.user_id == current_user.id).first())

    if not document:
        return APIResponse(
            status="failed",
            message="Document not found"
        )

    collection = mongodb[
        document.mongo_collection
    ]

    query = {}

    field_name = payload.column

    match  payload.operator:
        case "=":
            query[field_name] = payload.value
        case "contains":  
            query[field_name] = {"$regex": payload.value, "$options": "i"}
        case "startswith":
            query[field_name] = {"$regex": f"^{payload.value}", "$options": "i"}
        case "endswith":
            query[field_name] = {"$regex": f"{payload.value}$", "$options": "i"}
        case ">":
            query[field_name] = {"$gt": payload.value}
        case "<":
            query[field_name] = {"$lt": payload.value}
        case ">=":
            query[field_name] = {"$gte": payload.value}
        case "<=":
            query[field_name] = {"$lte": payload.value}

    skip = (payload.page - 1) * payload.page_size
    total = collection.count_documents(query)
    rows = list(collection.find(query, {"_id": 0}).skip(skip).limit(payload.page_size))

    return APIResponse(
        status="success",
        message="Search completed",
        data={
            "total": total,
            "page": payload.page,
            "page_size": payload.page_size,
            "results": rows
        }
    )
    
@router.get("/{document_id}/columns")
def get_document_columns(document_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    document = (db.query(Document).filter(Document.id == document_id, Document.user_id == current_user.id).first())

    if not document:
        return APIResponse(
            status="failed",
            message="Document not found"
        )

    collection = mongodb[
        document.mongo_collection
    ]

    first_row = collection.find_one()

    if not first_row:
        return APIResponse(
            status="failed",
            message="No data found"
        )

    columns = [key for key in first_row.keys() if key != "_id"]

    return APIResponse(
        status="success",
        message="Columns retrieved",
        data=columns
    )
    
@router.get("/{document_id}/sample")
def get_sample(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_cookie)
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == current_user.id
        )
        .first()
    )

    collection = mongodb[document.mongo_collection]

    sample = collection.find_one({}, {"_id": 0})

    return sample