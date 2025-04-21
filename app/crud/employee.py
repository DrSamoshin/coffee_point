from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

def get_employee(db: Session, employee_id: UUID):
    return db.query(Employee).filter(Employee.id == employee_id, Employee.active == True).first()

def get_employees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Employee).filter(Employee.active == True).offset(skip).limit(limit).all()

def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(name=employee.name)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, db_employee: Employee, updates: EmployeeUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_employee, field, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, db_employee: Employee):
    db_employee.active = False
    db.commit()
    db.refresh(db_employee)

def restore_employee(db: Session, employee_id: UUID):
    employee = db.query(Employee).filter(Employee.id == employee_id, Employee.active == False).first()
    if employee:
        employee.active = True
        db.commit()
        db.refresh(employee)
    return employee