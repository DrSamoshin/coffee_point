from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.db_sessions import get_point_db
from app.schemas.shift import ShiftOut
from app.crud import shift as crud_shift
from app.services.authentication import get_user_id_from_token


router = APIRouter(prefix='/shifts', tags=['shifts'])

@router.get("/", response_model=list[ShiftOut])
async def get_shifts(db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_shifts = crud_shift.get_shifts(db)
    return db_shifts

@router.get("/active-shifts/", response_model=list[ShiftOut])
async def get_active_shifts(db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_shifts = crud_shift.get_active_shifts(db)
    return db_shifts

@router.put("/shift-start-update/{shift_id}/", response_model=ShiftOut)
async def update_shift_start(shift_id: UUID, db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_shift = crud_shift.update_start_shift(db, shift_id)
    return db_shift
