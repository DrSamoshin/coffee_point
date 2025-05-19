from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.session import db_safe
from app.schemas.user import UserCreate, UserUpdate

@db_safe
def get_user(db: Session, user_id: UUID):
    return db.query(User).filter(User.id == user_id).first()

@db_safe
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

@db_safe
def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@db_safe
def update_user(db: Session, db_user: User, updates: UserUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@db_safe
def deactivate_user(db: Session, db_user: User):
    db_user.active = False
    db.commit()
    db.refresh(db_user)

@db_safe
def activate_user(db: Session, user_id: UUID):
    db_user = db.query(User).filter(User.id == user_id, User.active == False).first()
    if db_user:
        db_user.active = True
        db.commit()
        db.refresh(db_user)
    return db_user