import logging
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: UUID):
    logging.info("call method get_user")
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=500, detail="unexpected error during user fetch"
        )
    else:
        logging.info(f"user: {db_user}")
        if not db_user:
            raise HTTPException(status_code=404, detail="user not found")
        return db_user


def get_users(db: Session):
    logging.info("call method get_users")
    try:
        db_users = db.query(User).all()
    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=500, detail="unexpected error during users fetch"
        )
    else:
        logging.info(f"users: {len(db_users)}")
        return db_users


def create_user(db: Session, user: UserCreate):
    logging.info("call method create_user")
    try:
        db_user = User(name=user.name.strip(), db_name=user.db_name.strip())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=500, detail="unexpected error during user create"
        )
    else:
        logging.info(f"user is created: {db_user}")
        return db_user


def update_user(db: Session, user_id: UUID, updates: UserUpdate):
    logging.info("call method update_user")
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=500, detail="unexpected error during user update"
        )
    else:
        logging.info(f"user is updated: {db_user}")
        return db_user


def deactivate_user(db: Session, user_id: UUID):
    logging.info("call method deactivate_user")
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        db_user.deactivated = True
        db.commit()
        db.refresh(db_user)
    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=500, detail="unexpected error during user deactivate"
        )
    else:
        logging.info(f"user is deactivated: {db_user}")
        return db_user


def activate_user(db: Session, user_id: UUID):
    logging.info("call method activate_user")
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        db_user.deactivated = False
        db.commit()
        db.refresh(db_user)
    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=500, detail="unexpected error during user activate"
        )
    else:
        logging.info(f"user is activated: {db_user}")
        return db_user
