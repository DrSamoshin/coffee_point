from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import response
from app.db.session import get_db
from app.crud import employee as crud_employee
from app.schemas.employee import EmployeeCreate, EmployeeOut, EmployeeUpdate

router = APIRouter()

@router.post("/", response_model=EmployeeOut)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return crud_employee.create_employee(db, employee)

@router.get("/{employee_id}", response_model=EmployeeOut)
def read_employee(employee_id: str, db: Session = Depends(get_db)):
    db_employee = crud_employee.get_employee(db, UUID(employee_id))
    if not db_employee:
        return response("employee not found", 404, 'error')
    return db_employee

@router.get("/", response_model=List[EmployeeOut])
def read_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_employees = crud_employee.get_employees(db, skip, limit)
    return db_employees

@router.put("/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: str, user_update: EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = crud_employee.get_employee(db, UUID(employee_id))
    if not db_employee:
        return response("employee not found", 404, 'error')
    db_employee = crud_employee.update_employee(db, db_employee, user_update)
    return db_employee

@router.delete("/{employee_id}")
def delete_employee(employee_id: str, db: Session = Depends(get_db)):
    db_employee = crud_employee.get_employee(db, UUID(employee_id))
    if not db_employee:
        return response("employee not found", 404, 'error')
    crud_employee.delete_employee(db, db_employee)
    return response("employee deleted", 200, 'success')

@router.post("/{employee_id}/restore", response_model=EmployeeOut)
def restore_employee(employee_id: str, db: Session = Depends(get_db)):
    db_employee = crud_employee.restore_employee(db, UUID(employee_id))
    if not db_employee:
        return response("employee not found or already active", 404, 'error')
    return db_employee