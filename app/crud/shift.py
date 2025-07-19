import logging
from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.db.models import Shift
from app.db.db_sessions import db_safe


@db_safe
def get_shifts(db: Session):
    logging.info("call method get_shifts")
    try:
        db_shifts = db.query(Shift).order_by(desc(Shift.start_time)).filter().all()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"employee_shifts: {len(db_shifts)}")
        return db_shifts


@db_safe
def get_active_shifts(db: Session):
    logging.info("call method get_active_shifts")
    try:
        db_shifts = db.query(Shift).filter(Shift.active == True).all()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"active employee shifts: {len(db_shifts)}")
        return db_shifts


@db_safe
def update_start_shift(db: Session, shift_id: UUID):
    logging.info("call method update_start_shift")
    try:
        db_shift = db.query(Shift).filter(Shift.id == shift_id).first()
        db_shift.start_time = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_shift)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"shift is updated: {db_shift}")
        return db_shift
