import logging
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: UUID):
    logging.info(f"call method get_user")
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"users: {db_user}")
        return db_user

def get_users(db: Session):
    logging.info(f"call method get_users")
    try:
        db_users = db.query(User).all()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"users: {len(db_users)}")
        return db_users

def create_user(db: Session, user: UserCreate):
    logging.info(f"call method create_user")
    try:
        db_user = User(name=user.name, db_name=user.db_name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"user is created: {db_user}")
        return db_user

def update_user(db: Session, user_id: UUID, updates: UserUpdate):
    logging.info(f"call method update_user")
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"user is updated: {db_user}")
        return db_user

def deactivate_user(db: Session, user_id: UUID):
    logging.info(f"call method deactivate_user")
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        db_user.deactivated = True
        db.commit()
        db.refresh(db_user)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"user is deactivated: {db_user}")
        return db_user
