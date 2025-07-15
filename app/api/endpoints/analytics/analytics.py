import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import analytics as crud_analytics
from app.db.db_sessions import get_point_db
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/shift-report/{shift_id}/")
async def get_shift_report(
    shift_id: UUID,
    db: Session = Depends(get_point_db),
    user_id: str = Depends(get_user_id_from_token),
):
    try:
        db_shift_report = crud_analytics.get_shift_report(db, shift_id)
    except HTTPException as http_exc:
        logging.error(f"{http_exc}")
        raise http_exc
    else:
        logging.info(f"shift report: {db_shift_report}")
        return db_shift_report


@router.get("/active-shift-report/")
async def get_active_shift_report(
    db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)
):
    try:
        db_active_shift_report = crud_analytics.get_active_shift_report(db)
    except HTTPException as http_exc:
        logging.error(f"{http_exc}")
        raise http_exc
    else:
        logging.info(f"active shift report: {db_active_shift_report}")
        return db_active_shift_report
