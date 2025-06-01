import logging
from uuid import UUID
from sqlalchemy.orm import Session
from app.db.models import Employee
from app.db.session import db_safe
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.core.consts import EmployeePosition


@db_safe
def get_employee(db: Session, employee_id: UUID):
    return db.query(Employee).filter(Employee.id == employee_id).first()

# +
@db_safe
def get_employees(db: Session):
    return db.query(Employee).filter(Employee.deactivated == False).all()

@db_safe
def get_baristas(db: Session):
    return db.query(Employee).filter(Employee.deactivated == False,
                                     Employee.position == EmployeePosition.barista).all()

@db_safe
def get_deactivated_employees(db: Session):
    return db.query(Employee).filter(Employee.deactivated == True).offset(skip).limit(limit).all()

# +
@db_safe
def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(name=employee.name,
                           position=employee.position)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    logging.info(f"Employee is created: {db_employee}")
    return db_employee

@db_safe
def update_employee(db: Session, db_employee: Employee, updates: EmployeeUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_employee, field, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@db_safe
def deactivate_employee(db: Session, db_employee: Employee):
    db_employee.deactivated = True
    db.commit()
    db.refresh(db_employee)

@db_safe
def activate_employee(db: Session, employee_id: UUID):
    employee = db.query(Employee).filter(Employee.id == employee_id, Employee.deactivated == True).first()
    if employee:
        employee.active = True
        db.commit()
        db.refresh(employee)
    return employee