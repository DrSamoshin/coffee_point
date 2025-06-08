from typing import Optional, Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.shift import ShiftOut, ShiftStartUpdate, ShiftEndUpdate
from app.crud import shift as crud_shift
from app.core.responses import response
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/shifts', tags=['shifts'])

# @router.post("/", response_model=ShiftOut)
# async def create_shift(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
#     return crud_shift.create_shift(db)

# manager_app
@router.get("/", response_model=list[ShiftOut])
async def get_shifts(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    shifts = crud_shift.get_shifts(db)
    return shifts

# barista_app
@router.get("/active-shift/", response_model=Union[ShiftOut, None])
async def get_active_shift(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    return crud_shift.get_active_shift(db)

# @router.get("/{shift_id}/", response_model=ShiftOut)
# async def get_shift(shift_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
#     shift = crud_shift.get_shift(db, UUID(shift_id))
#     if not shift:
#         return response("shift not found", 404, "error")
#     return shift

# barista_app
@router.put("/shift-start-update/{shift_id}/", response_model=ShiftOut)
async def update_shift_start(shift_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    shift = crud_shift.get_shift(db, UUID(shift_id))
    if not shift:
        return response("shift not found", 404, "error")
    shift = crud_shift.update_start_shift(db, shift)
    return shift

# @router.put("/shift-end-update/{shift_id}/", response_model=ShiftOut)
# async def update_shift_end(shift_id: str, shift_update: ShiftEndUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
#     shift = crud_shift.get_shift(db, UUID(shift_id))
#     if not shift:
#         return response("shift not found", 404, "error")
#     shift = crud_shift.update_end_shift(db, shift, shift_update)
#     return shift
