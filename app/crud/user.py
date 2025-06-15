import logging
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.session import db_safe
from app.schemas.user import UserCreate, UserUpdate

@db_safe
def get_user(db: Session, user_id: UUID):
    return db.query(User).filter(User.id == user_id).first()

@db_safe
def get_users(db: Session):
    return db.query(User).all()

@db_safe
def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@db_safe
def update_user(db: Session, user_id: UUID, updates: UserUpdate):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as error:
        logging.warning(error)

@db_safe
def deactivate_user(db: Session, user_id: UUID):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        db_user.deactivated = True
        db.commit()
        db.refresh(db_user)
    except Exception as error:
        logging.warning(error)

@db_safe
def activate_user(db: Session, user_id: UUID):
    db_user = db.query(User).filter(User.id == user_id, User.deactivated == True).first()
    if db_user:
        db_user.deactivated = False
        db.commit()
        db.refresh(db_user)
    return db_user