from fastapi import APIRouter, Depends
from core.Models import User, Document
from core.functions import get_current_user_from_cookie
from auth.jwt_handler import is_admin
from db.database import get_db
from sqlalchemy.orm import Session
from schema.admin_schema import UsersOutputSchema, APIResponse, UpdateUserDataInputSchema

router = APIRouter(
    prefix='/admin',
    tags=['ADMIN']
)

def check_admin_permission_required(obj) -> bool:
    obj = {
        "email": obj.email,
        "user_id": obj.id,
        "username": obj.username,
        "is_admin": obj.is_admin
    }
    
    res = is_admin(obj)
    
    return res

@router.get('/users', response_model=UsersOutputSchema)
def get_users(current_user: User = Depends(get_current_user_from_cookie),  db: Session = Depends(get_db)):

    if not check_admin_permission_required(current_user):
        return UsersOutputSchema(
            status='failed',
            message='Forbidden: You dont have access to this resources',
        )
     
    users = db.query(User).order_by(User.id).all()
    
    if not users:
        return UsersOutputSchema(
            status="success",
            message="No user found"
        )
        
    return UsersOutputSchema(
        status="success",
        message="List of users",
        data= [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_acitve": user.is_active
            }
            
            for user in users
        ]
    )
    
@router.get('/users/{id}', response_model='')
def get_single_user(
    id: int, 
    current_user: User = Depends(get_current_user_from_cookie), 
    db:Session = Depends(get_db)
):  
    if not check_admin_permission_required(current_user):
        return UsersOutputSchema(
            status='failed',
            message='Forbidden: You do not have access to this resource',
        )
        
    user = db.query(User).filter(User.id == id).first()
    
    if not user:
        return UsersOutputSchema(
            status='failed',
            message='No user found'
        )
        
    return UsersOutputSchema(
        status='success',
        message='User record found',
        data=[{
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_acitve": user.is_active
        }]
    )
    
@router.delete('/users/{user_id}/delete', response_model=APIResponse)
def delete_user(user_id: int,current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    if not check_admin_permission_required(current_user):
        return APIResponse(
            status='failed',
            message='Forbidden: You do not have access to this resource'
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        return APIResponse(
            status='failed',
            message='No user found'
        )
        
    db.delete(user)
    db.commit()
    
    return APIResponse(
        status='success',
        message='User deleted successfully' 
    )
    
@router.patch('/users/{user_id}/update', response_model=APIResponse)
def update_user(payload: UpdateUserDataInputSchema, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    if not check_admin_permission_required(current_user):
        return APIResponse(
            status='failed',
            message='Forbidden: You dont have access to this resources',
        )
        
    user = db.query(User).filter(User.email == payload.email).first()
    if not user: 
        return APIResponse(
            status='failed',
            message='No record found'
        )
        
    updated_user_info = db.query(User).update({User.data[0]: data[1] for data in payload.data})
    
    db.commit()
    db.refresh(updated_user_info)
    
    return APIResponse(
        status='success',
        message='User data updated successfully'
    )

#for documents
@router.get('/documents', response_model=APIResponse)
def get_documents(current_user: User = Depends(get_current_user_from_cookie), db:Session = Depends(get_db)):
    if not check_admin_permission_required(current_user):
        return APIResponse(
            status='failed',
            message='Forbidden: You do not have access to this resource'
        )
        
    documents = db.query(Document).order_by(Document.created_at.desc()).all()      
      
    if not documents:
        return APIResponse(
            status="success",
            message="No document found"
        )
        
    return APIResponse(
        status='success',
        message='List of documents',
        data= [
            {
                "id": doc.id,
                "user_id": doc.user_id,
                "filename": doc.filename,
                "mongo_collection": doc.mongo_collection,
                "rows_count": doc.rows_count,
                "columns_count": doc.columns_count,
                "created_at": doc.created_at
            }
            for doc in documents
        ]
    )
    
@router.get('/documents/{user_id}', response_model=APIResponse)
def get_documents(user_id: int, current_user: User = Depends(get_current_user_from_cookie), db:Session = Depends(get_db)):
    if not check_admin_permission_required(current_user):
        return APIResponse(
            status='failed',
            message='Forbidden: You do not have access to this resource'
        )
        
    documents = db.query(Document).filter(Document.user_id == user_id).order_by(Document.created_at.desc()).all()      
      
    if not documents:
        return APIResponse(
            status="success",
            message="No document found"
        )
        
    return APIResponse(
        status='success',
        message='List of documents',
        data= [
            {
                "id": doc.id,
                "user_id": doc.user_id,
                "filename": doc.filename,
                "mongo_collection": doc.mongo_collection,
                "rows_count": doc.rows_count,
                "columns_count": doc.columns_count,
                "created_at": doc.created_at
            }
            for doc in documents
        ]
    )
    
@router.delete('/document/{document_id}/detail', response_model=APIResponse)
def delete_document(document_id: int, current_user: User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    if not check_admin_permission_required(current_user):
        return APIResponse(
            status='failed',
            message='Forbidden: You do not have access to this resource'
        )
        
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        return APIResponse(
            status='failed',
            message='No document found'
        )

    db.delete(document)
    db.commit()
    
    return APIResponse(
        status='success',
        message=f'Document with ID: {document_id} deleted successfully'
    )