from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.core.responses import response
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/users', tags=['users'])

@router.get("/", response_model=List[UserOut])
async def get_users(db: Session = Depends(get_db), auth_user_id: str = Depends(get_user_id_from_token)):
    db_users = crud_user.get_users(db)
    return db_users

@router.get("/{user_id}/", response_model=UserOut)
async def get_user(user_id: str, db: Session = Depends(get_db), auth_user_id: str = Depends(get_user_id_from_token)):
    db_user = crud_user.get_user(db, UUID(user_id))
    return db_user

@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db), auth_user_id: str = Depends(get_user_id_from_token)):
    db_user = crud_user.create_user(db, user)
    return db_user

@router.put("/{user_id}/", response_model=UserOut)
async def update_user(user_id: UUID, user_update: UserUpdate, db: Session = Depends(get_db), auth_user_id: str = Depends(get_user_id_from_token)):
    db_user = crud_user.update_user(db, user_id, user_update)
    return db_user

@router.delete("/{user_id}/")
async def deactivate_user(user_id: UUID, db: Session = Depends(get_db), auth_user_id: str = Depends(get_user_id_from_token)):
    db_user = crud_user.deactivate_user(db, user_id)
    return db_user