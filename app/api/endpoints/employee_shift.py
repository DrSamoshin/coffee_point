from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.employee_shift import EmployeeShiftCreate, EmployeeShiftOut, EmployeeShiftUpdate
from app.crud import employee_shift as crud_employee_shift
from app.core.responses import response
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/employee_shifts', tags=['employee_shifts'])

# barista_app
@router.post("/", response_model=EmployeeShiftOut)
async def create_employee_shift(employee_shifts: EmployeeShiftCreate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    return crud_employee_shift.create_employee_shift(db, employee_shifts)

# manager_app
@router.get("/", response_model=list[EmployeeShiftOut])
async def get_employee_shifts(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    shifts = crud_employee_shift.get_employee_shifts(db)
    return shifts

# barista_app
@router.get("/active-employee-shifts/", response_model=list[EmployeeShiftOut])
async def get_active_employee_shifts(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    shifts = crud_employee_shift.get_active_employee_shifts(db)
    return shifts

# @router.get("/{shift_id}/", response_model=EmployeeShiftOut)
# async def read_shift(shift_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
#     shift = crud_employee_shift.get_employee_shift(db, UUID(shift_id))
#     if not shift:
#         return response("shift not found", 404, "error")
#     return shift

# barista_app
@router.put("/shift-end-update/{shift_id}/", response_model=EmployeeShiftOut)
async def update_employee_shift_end(shift_id: str, shift_update: EmployeeShiftUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    # shift = crud_employee_shift.get_employee_shift(db, UUID(shift_id))
    # if not shift:
    #     return response("shift not found", 404, "error")
    shift = crud_employee_shift.update_employee_shift_end(db, shift_id, shift_update)
    return shift
