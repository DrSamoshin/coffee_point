import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.analytics import ShiftIncomeOut
from app.crud import analytics as crud_analytics
from app.db.db_sessions import get_point_db
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/shift-income/{shift_id}/", response_model=ShiftIncomeOut)
async def get_shift_income(shift_id: UUID, db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    try:
        db_shift_income = crud_analytics.get_shift_income(db, shift_id)
    except HTTPException as http_exc:
        logging.error(f"{http_exc}")
        raise http_exc
    else:
        logging.info(f"shift income: {db_shift_income}")
        return db_shift_income

@router.get("/active-shift-income/", response_model=ShiftIncomeOut)
async def get_active_shift_income(db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    try:
        db_shift_income = crud_analytics.get_active_shift_income(db)
    except HTTPException as http_exc:
        logging.error(f"{http_exc}")
        raise http_exc
    else:
        logging.info(f"active shift income: {db_shift_income}")
        return db_shift_income

@router.get("/active-shift-orders/{shift_id}/")
async def get_shift_orders(shift_id: UUID, db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_shift_income = crud_analytics.get_shift_orders(db, shift_id)
    return db_shift_income