import logging
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.responses import response
from app.db.db_sessions import get_users_db
from app.crud import user as crud_user
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/app/")
async def get_health_check():
    msg = "application is running"
    logging.info(msg)
    return response(msg)


@router.get("/token/")
async def check_token(
    db: Session = Depends(get_users_db), user_id: UUID = Depends(get_user_id_from_token)
):
    try:
        db_user = crud_user.get_user(db=db, user_id=user_id)
    except HTTPException as http_exc:
        logging.error(f"{http_exc}")
        raise http_exc
    else:
        msg = f"token is valid. user: {db_user.name}"
        logging.info(msg)
        return response(msg)
