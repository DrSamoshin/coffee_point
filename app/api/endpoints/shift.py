from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.shift import ShiftCreate, ShiftOut, ShiftUpdate
from app.crud import shift as crud_shift
from app.core.responses import response

router = APIRouter(prefix='/shifts', tags=['shifts'])

@router.post("/", response_model=ShiftOut)
def create_shift(shift: ShiftCreate, db: Session = Depends(get_db)):
    return crud_shift.create_shift(db, shift)

@router.get("/", response_model=list[ShiftOut])
def read_shifts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    shifts = crud_shift.get_shifts(db, skip, limit)
    return shifts

@router.get("/{shift_id}", response_model=ShiftOut)
def read_shift(shift_id: str, db: Session = Depends(get_db)):
    shift = crud_shift.get_shift(db, UUID(shift_id))
    if not shift:
        return response("shift not found", 404, "error")
    return shift

@router.put("/{shift_id}", response_model=ShiftOut)
def update_shift(shift_id: str, shift_update: ShiftUpdate, db: Session = Depends(get_db)):
    shift = crud_shift.get_shift(db, UUID(shift_id))
    if not shift:
        return response("shift not found", 404, "error")
    shift = crud_shift.update_shift(db, shift, shift_update)
    return shift
