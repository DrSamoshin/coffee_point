from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.core.responses import response

router = APIRouter()

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user)

@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, UUID(user_id))
    if not db_user:
        return response("user not found", 404, "error")
    return db_user

@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_user.get_users(db, skip, limit)

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, UUID(user_id))
    if not db_user:
        return response("user not found", 404, "error")
    return crud_user.update_user(db, db_user, user_update)

@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, UUID(user_id))
    if not db_user:
        return response("user not found", 404, "error")
    crud_user.deactivate_user(db, db_user)
    return response("user deleted", 200, 'success')

@router.post("/{user_id}/restore", response_model=UserOut)
def restore_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud_user.activate_user(db, UUID(user_id))
    if not db_user:
        return response("user not found or already active", 404, 'error')
    return db_user