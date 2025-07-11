import logging
import os
import subprocess
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.db_sessions import get_users_db
from app.core.responses import response
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/users', tags=['users'])

@router.get("/", response_model=List[UserOut])
async def get_users(db: Session = Depends(get_users_db), auth_user_id: str = Depends(get_user_id_from_token)):
    try:
        db_users = crud_user.get_users(db)
    except HTTPException as http_exc:
        logging.error(f"{http_exc}")
        raise http_exc
    else:
        logging.info(f"users: {len(db_users)}")
        return db_users

@router.get("/{user_id}/", response_model=UserOut)
async def get_user(user_id: UUID, db: Session = Depends(get_users_db), auth_user_id: str = Depends(get_user_id_from_token)):
    try:
        db_user = crud_user.get_user(db, user_id)
    except HTTPException as http_exc:
        logging.error(f"{http_exc}")
        raise http_exc
    else:
        logging.info(f"user: {db_user}")
        return db_user

@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_users_db), auth_user_id: str = Depends(get_user_id_from_token)):
    db_user = crud_user.create_user(db, user)
    return db_user

@router.put("/{user_id}/", response_model=UserOut)
async def update_user(user_id: UUID, user_update: UserUpdate, db: Session = Depends(get_users_db), auth_user_id: str = Depends(get_user_id_from_token)):
    try:
        db_user = crud_user.update_user(db, user_id, user_update)
    except HTTPException as http_exc:
        logging.error(f"{http_exc}")
        raise http_exc
    else:
        logging.info(f"user: {db_user}")
        return db_user

@router.delete("/{user_id}/")
async def deactivate_user(user_id: UUID, db: Session = Depends(get_users_db), auth_user_id: str = Depends(get_user_id_from_token)):
    try:
        db_user = crud_user.deactivate_user(db, user_id)
    except HTTPException as http_exc:
        logging.error(f"{http_exc}")
        raise http_exc
    else:
        logging.info(f"user: {db_user}")
        return db_user

@router.get("/migrate-users-db/")
def migrate_users_db(user_id: UUID = Depends(get_user_id_from_token)):
    try:
        result = subprocess.run(
            ["alembic", "-c", "alembic_users_db/alembic.ini", "upgrade", "head"],
            capture_output=True,
            text=True,
            check=True
        )
        logging.info(result)
        return response("db is migrated", 200, "success")
    except subprocess.CalledProcessError as e:
        return response("db is not migrated", 500, f"error: {str(e)}")

@router.get("/migrate-point-db/{db_name}/")
def migrate_point_db(db_name: str, user_id: UUID = Depends(get_user_id_from_token)):
    try:
        os.environ["TARGET_DB_NAME"] = db_name
        logging.info(os.environ.get("TARGET_DB_NAME"))
        result = subprocess.run(
            ["alembic", "-c", "alembic_points_db/alembic.ini", "upgrade", "head"],
            capture_output=True,
            text=True,
            check=True
        )
        logging.info(result)
        return response("db is migrated", 200, "success")
    except subprocess.CalledProcessError as e:
        return response("db is not migrated", 500, f"error: {str(e)}")