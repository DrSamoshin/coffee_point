from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.analytics import ShiftIncomeOut
from app.crud import analytics as crud_analytics
from app.db.db_sessions import get_point_db
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/{shift_id}/", response_model=ShiftIncomeOut)
async def get_shift_income(shift_id: UUID, db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_shift_income = crud_analytics.get_shift_income(db, shift_id)
    return db_shift_income