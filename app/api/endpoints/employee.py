import logging
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.responses import response
from app.db.session import get_db
from app.crud import employee as crud_employee
from app.services.authentication import get_user_id_from_token
from app.schemas.employee import EmployeeCreate, EmployeeOut, EmployeeUpdate, BaristaOut

router = APIRouter(prefix='/employees', tags=['employees'])

# manager_app
@router.post("/", response_model=EmployeeOut)
async def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    return crud_employee.create_employee(db, employee)

# barista_app
@router.get("/", response_model=List[EmployeeOut])
async def get_employees(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    employees = crud_employee.get_employees(db)
    return employees

# @router.get("/baristas/", response_model=List[BaristaOut])
# async def get_baristas(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
#     baristas = crud_employee.get_baristas(db)
#     return baristas

# @router.get("/{employee_id}/", response_model=EmployeeOut)
# async def read_employee(employee_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
#     db_employee = crud_employee.get_employee(db, UUID(employee_id))
#     if not db_employee:
#         return response("employee not found", 404, 'error')
#     return db_employee

# @router.put("/{employee_id}/", response_model=EmployeeOut)
# async def update_employee(employee_id: str, user_update: EmployeeUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
#     db_employee = crud_employee.get_employee(db, UUID(employee_id))
#     if not db_employee:
#         return response("employee not found", 404, 'error')
#     db_employee = crud_employee.update_employee(db, db_employee, user_update)
#     return db_employee

# @router.delete("/{employee_id}/")
# async def deactivate_employee(employee_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
#     db_employee = crud_employee.get_employee(db, UUID(employee_id))
#     if not db_employee:
#         return response("employee not found", 404, 'error')
#     crud_employee.deactivate_employee(db, db_employee)
#     return response("employee deleted", 200, 'success')

# @router.get("/{employee_id}/activate/", response_model=EmployeeOut)
# async def activate_employee(employee_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
#     db_employee = crud_employee.activate_employee(db, UUID(employee_id))
#     if not db_employee:
#         return response("employee not found or already active", 404, 'error')
#     return db_employee