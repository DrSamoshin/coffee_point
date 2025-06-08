import logging
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.db.models import Shift
from app.db.models.employee_shift import EmployeeShift
from app.db.session import db_safe
from app.schemas.employee_shift import EmployeeShiftCreate, EmployeeShiftUpdate


# +
@db_safe
def get_employee_shift(db: Session, employee_shift_id: UUID):
    return db.query(EmployeeShift).filter(EmployeeShift.id == employee_shift_id).first()

# +
@db_safe
def get_employee_shifts(db: Session):
    return db.query(EmployeeShift).filter().all()

# +
@db_safe
def get_active_employee_shifts(db: Session):
    return db.query(EmployeeShift).filter(EmployeeShift.active == True).all()

# @db_safe
# def get_deactivated_employee_shifts(db: Session):
#     return db.query(EmployeeShift).filter(EmployeeShift.active == False).all()

# +
@db_safe
def create_employee_shift(db: Session, employee_shift: EmployeeShiftCreate):
    logging.info(employee_shift.shift_id)
    if shift_id:=employee_shift.shift_id:
        db_employee_shift = EmployeeShift(start_time=datetime.now(),
                                          employee_id=employee_shift.employee_id,
                                          shift_id=shift_id)
        db.add(db_employee_shift)
        db.commit()
        db.refresh(db_employee_shift)
        logging.info(f"Employee shift is created: {db_employee_shift}")
        return db_employee_shift
    else:
        try:
            with db.begin():
                db_shift = Shift()
                db.add(db_shift)
                db.flush()

                db_employee_shift = EmployeeShift(start_time=datetime.now(),
                                                  employee_id=employee_shift.employee_id,
                                                  shift_id=db_shift.id)
                db.add(db_employee_shift)
            return db_employee_shift
        except Exception as e:
            db.rollback()
            raise e

# +
@db_safe
def update_employee_shift_end(db: Session, shift_id: str, updates: EmployeeShiftUpdate):
    db_employee_shift = db.query(EmployeeShift).filter(EmployeeShift.id == shift_id).options(
        joinedload(EmployeeShift.shift)).first()
    if updates.last_employee_shift:
        db_employee_shift.end_time = datetime.now()
        db_employee_shift.active = False
        db_employee_shift.shift.end_time = datetime.now()
        db_employee_shift.shift.active = False
        db.commit()
        db.refresh(db_employee_shift)
        logging.info(f"Last employee shift and shift is closed: {db_employee_shift}")
    else:
        db_employee_shift.end_time = datetime.now()
        db_employee_shift.active = False
        db.commit()
        db.refresh(db_employee_shift)
        logging.info(f"Employee shift is closed: {db_employee_shift}")
    return db_employee_shift

