from datetime import timedelta
from uuid import UUID

from sqlalchemy.orm import Session
from app.db.models import Shift
from app.db.session import db_safe
from app.schemas.shift import ShiftCreate, ShiftUpdate

@db_safe
def get_shift(db: Session, shift_id: UUID):
    return db.query(Shift).filter(Shift.id == shift_id).first()

@db_safe
def get_shifts(db: Session, skip=0, limit=10):
    return db.query(Shift).filter(Shift.active == True).offset(skip).limit(limit).all()

@db_safe
def get_deactivated_shifts(db: Session, skip=0, limit=10):
    return db.query(Shift).filter(Shift.active == False).offset(skip).limit(limit).all()

@db_safe
def create_shift(db: Session, shift: ShiftCreate):
    data = shift.model_dump()
    if not data.get("end_time"):
        data["end_time"] = data["start_time"] + timedelta(hours=12)
    db_shift = Shift(**data)
    db.add(db_shift)
    db.commit()
    db.refresh(db_shift)
    return db_shift

@db_safe
def update_shift(db: Session, db_shift: Shift, updates: ShiftUpdate):
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_shift, key, value)
    db.commit()
    db.refresh(db_shift)
    return db_shift

@db_safe
def deactivate_shift(db: Session, db_shift: Shift):
    db_shift.active = False
    db.commit()
    db.refresh(db_shift)

@db_safe
def activate_shift(db: Session, shift_id: UUID):
    db_shift = db.query(Shift).filter(Shift.id == shift_id, Shift.active == False).first()
    if db_shift:
        db_shift.active = True
        db.commit()
        db.refresh(db_shift)
    return db_shift
