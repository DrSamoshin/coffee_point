import logging
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Employee, EmployeeShift
from app.db.db_sessions import db_safe
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


@db_safe
def get_employees(db: Session):
    logging.info("call method get_employees")
    try:
        db_employees = (
            db.query(Employee)
            .filter(Employee.deactivated is False)
            .order_by(Employee.name)
            .all()
        )
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"employees: {len(db_employees)}")
        return db_employees


@db_safe
def get_deactivated_employees(db: Session):
    logging.info("call method get_deactivated_employees")
    try:
        db_employees = (
            db.query(Employee)
            .filter(Employee.deactivated is True)
            .order_by(Employee.name)
            .all()
        )
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"deactivated employees: {len(db_employees)}")
        return db_employees


@db_safe
def get_available_employees(db: Session):
    logging.info("call method get_available_employees")
    try:
        db_active_shifts = (
            db.query(EmployeeShift).filter(EmployeeShift.active is True).all()
        )
        active_employee_ids = [shift.employee_id for shift in db_active_shifts]
        db_employees = (
            db.query(Employee)
            .filter(Employee.deactivated is False)
            .order_by(Employee.name)
            .all()
        )
        active_employees = [
            employee
            for employee in db_employees
            if employee.id not in active_employee_ids
        ]
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"active_employees: {len(active_employees)}")
        return active_employees


@db_safe
def create_employee(db: Session, employee: EmployeeCreate):
    logging.info("call method create_employee")
    try:
        db_employee = Employee(name=employee.name.strip(), position=employee.position)
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"employee is created: {db_employee}")
        return db_employee


@db_safe
def update_employee(db: Session, employee_id: UUID, updates: EmployeeUpdate):
    logging.info("call method update_employee")
    try:
        db_employee = (
            db.query(Employee)
            .filter(Employee.id == employee_id, Employee.deactivated is False)
            .first()
        )
        for field, value in updates.model_dump().items():
            setattr(db_employee, field, value)
        db.commit()
        db.refresh(db_employee)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"employee is updated: {db_employee}")
        return db_employee


@db_safe
def deactivate_employee(db: Session, employee_id: UUID):
    logging.info("call method deactivate_employee")
    try:
        db_employee = (
            db.query(Employee)
            .filter(Employee.id == employee_id, Employee.deactivated is False)
            .first()
        )
        db_employee.deactivated = True
        db.commit()
        db.refresh(db_employee)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"employee is deactivated: {db_employee}")
        return db_employee


@db_safe
def activate_employee(db: Session, employee_id: UUID):
    logging.info("call method activate_employee")
    try:
        db_employee = (
            db.query(Employee)
            .filter(Employee.id == employee_id, Employee.deactivated is True)
            .first()
        )
        db_employee.deactivated = False
        db.commit()
        db.refresh(db_employee)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"employee is activated: {db_employee}")
        return db_employee
