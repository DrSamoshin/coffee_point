from datetime import timedelta
from uuid import UUID

from sqlalchemy.orm import Session
from app.db.models import Shift
from app.schemas.shift import ShiftCreate, ShiftUpdate

def create_shift(db: Session, shift: ShiftCreate):
    data = shift.model_dump()
    if not data.get("end_time"):
        data["end_time"] = data["start_time"] + timedelta(hours=12)
    db_shift = Shift(**data)
    db.add(db_shift)
    db.commit()
    db.refresh(db_shift)
    return db_shift

def get_shift(db: Session, shift_id: UUID):
    return db.query(Shift).filter(Shift.id == shift_id).first()

def get_shifts(db: Session, skip=0, limit=10):
    return db.query(Shift).offset(skip).limit(limit).all()

def update_shift(db: Session, db_shift: Shift, updates: ShiftUpdate):
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_shift, key, value)
    db.commit()
    db.refresh(db_shift)
    return db_shift
