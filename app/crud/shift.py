import logging
from uuid import UUID

from sqlalchemy.orm import Session
from app.db.models import Shift
from app.db.session import db_safe
from app.schemas.shift import ShiftCreate, ShiftUpdate


@db_safe
def get_shift(db: Session, shift_id: UUID):
    return db.query(Shift).filter(Shift.id == shift_id).first()

@db_safe
def get_shifts(db: Session):
    return db.query(Shift).filter().all()

@db_safe
def get_active_shifts(db: Session):
    return db.query(Shift).filter(Shift.active == True).all()

@db_safe
def get_deactivated_shifts(db: Session):
    return db.query(Shift).filter(Shift.active == False).all()

@db_safe
def create_shift(db: Session, shift: ShiftCreate):
    data = shift.model_dump()
    db_shift = Shift(**data)
    db.add(db_shift)
    db.commit()
    db.refresh(db_shift)
    logging.info(f"Shift is created: {db_shift}")
    return db_shift

@db_safe
def update_shift(db: Session, db_shift: Shift, updates: ShiftUpdate):
    db_shift.end_time = updates.end_time
    db_shift.active = False
    db.commit()
    db.refresh(db_shift)
    logging.info(f"Shift is closed: {db_shift}")
    return db_shift
