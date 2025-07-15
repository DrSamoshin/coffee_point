from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.db_sessions import get_point_db
from app.crud import employee as crud_employee
from app.services.authentication import get_user_id_from_token
from app.schemas.employee import EmployeeCreate, EmployeeOut, EmployeeUpdate

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=List[EmployeeOut])
async def get_employees(
    db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)
):
    employees = crud_employee.get_employees(db)
    return employees


@router.get("/deactivated/", response_model=List[EmployeeOut])
async def get_deactivated_employees(
    db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)
):
    employees = crud_employee.get_deactivated_employees(db)
    return employees


@router.get("/available/", response_model=List[EmployeeOut])
async def get_available_employees(
    db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)
):
    employees = crud_employee.get_available_employees(db)
    return employees


@router.post("/", response_model=EmployeeOut)
async def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_point_db),
    user_id: str = Depends(get_user_id_from_token),
):
    db_employee = crud_employee.create_employee(db, employee)
    return db_employee


@router.put("/{employee_id}/", response_model=EmployeeOut)
async def update_employee(
    employee_id: UUID,
    user_update: EmployeeUpdate,
    db: Session = Depends(get_point_db),
    user_id: str = Depends(get_user_id_from_token),
):
    db_employee = crud_employee.update_employee(db, employee_id, user_update)
    return db_employee


@router.delete("/{employee_id}/", response_model=EmployeeOut)
async def deactivate_employee(
    employee_id: UUID,
    db: Session = Depends(get_point_db),
    user_id: str = Depends(get_user_id_from_token),
):
    db_employee = crud_employee.deactivate_employee(db, employee_id)
    return db_employee


@router.post("/activate/{employee_id}/", response_model=EmployeeOut)
async def activate_employee(
    employee_id: UUID,
    db: Session = Depends(get_point_db),
    user_id: str = Depends(get_user_id_from_token),
):
    db_employee = crud_employee.activate_employee(db, employee_id)
    return db_employee
