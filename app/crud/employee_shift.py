import logging
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.db.models import Shift
from app.db.models.employee_shift import EmployeeShift
from app.db.session import db_safe
from app.schemas.employee_shift import EmployeeShiftCreate, EmployeeShiftUpdate


@db_safe
def get_employee_shifts(db: Session):
    logging.info(f"call method get_employee_shifts")
    try:
        db_employee_shifts = db.query(EmployeeShift).filter().all()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"employee_shifts: {len(db_employee_shifts)}")
        return db_employee_shifts

@db_safe
def get_active_employee_shifts(db: Session):
    logging.info(f"call method get_active_employee_shifts")
    try:
        db_active_employee_shifts = db.query(EmployeeShift).filter(EmployeeShift.active == True).options(
        joinedload(EmployeeShift.employee)).all()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"active_employee_shifts: {len(db_active_employee_shifts)}")
        return db_active_employee_shifts

@db_safe
def create_employee_shift(db: Session, employee_shift: EmployeeShiftCreate):
    logging.info(f"call method create_employee_shift")
    try:
        with db.begin():
            if employee_shift.shift_id:
                shift_id = employee_shift.shift_id
            else:
                db_shift = Shift()
                db.add(db_shift)
                db.flush()
                shift_id = db_shift.id

            db_employee_shift = EmployeeShift(start_time=datetime.now(),
                                              employee_id=employee_shift.employee_id,
                                              shift_id=shift_id)
            db.add(db_employee_shift)
        db.refresh(db_employee_shift)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"employee_shift is created: {db_employee_shift}")
        return db_employee_shift

@db_safe
def update_employee_shift_end(db: Session, shift_id: str, updates: EmployeeShiftUpdate):
    logging.info(f"call method update_employee_shift_end")
    try:
        db_employee_shift = db.query(EmployeeShift).filter(EmployeeShift.id == shift_id).options(
            joinedload(EmployeeShift.shift)).first()
        if updates.last_employee_shift:
            db_employee_shift.end_time = datetime.now()
            db_employee_shift.active = False
            db_employee_shift.shift.end_time = datetime.now()
            db_employee_shift.shift.active = False
            db.commit()
            db.refresh(db_employee_shift)
            logging.info(f"last employee shift and shift is closed: {db_employee_shift}")
        else:
            db_employee_shift.end_time = datetime.now()
            db_employee_shift.active = False
            db.commit()
            db.refresh(db_employee_shift)
            logging.info(f"employee shift is closed: {db_employee_shift}")
    except Exception as error:
        logging.error(error)
    else:
        return db_employee_shift
