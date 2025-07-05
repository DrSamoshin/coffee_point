import logging
import os

from fastapi import HTTPException
from functools import wraps
from sqlalchemy import create_engine
from uuid import UUID
from app.crud import user as crud_user
from fastapi import Depends
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.core.configs import settings
from app.services.authentication import get_user_id_from_token

POINT_DB_ENGINES = dict()
USERS_DB_ENGINES = dict()
POINT_URLS = dict()


def create_db_engine(url: str, pool_size: int = 3, max_overflow: int = 1):
    return create_engine(
        url,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=30,
        pool_recycle=1800
    )

def get_db_session(user_db_engine):
    session = sessionmaker(autocommit=False, autoflush=False, bind=user_db_engine)
    return session()

def check_users_db_availability():
    try:
        users_db_engine = create_db_engine(settings.data_base.get_db_url('users'))
        users_db_engine.connect()
        logging.info(f"users DB is available")
    except OperationalError as error:
        settings.data_base.DB_AVAILABLE = False
        logging.info(error)
        logging.warning(f"users DB is not available")

def get_point_db_url(user_id: UUID):
    if not POINT_URLS.get(user_id):
        users_db_engine = get_users_db_engine()
        db = get_db_session(users_db_engine)
        db_user = crud_user.get_user(db=db, user_id=user_id)
        user_db_name = db_user.db_name
        user_db_url = settings.data_base.get_db_url(user_db_name)
        POINT_URLS[user_id] = user_db_url
    return POINT_URLS.get(user_id)

def get_point_db_engine(user_id: UUID):
    if not POINT_DB_ENGINES.get(user_id):
        user_db_url = get_point_db_url(user_id)
        user_engine = create_db_engine(user_db_url)
        POINT_DB_ENGINES[user_id] = user_engine
    return POINT_DB_ENGINES.get(user_id)

def get_point_db(user_id: UUID = Depends(get_user_id_from_token)):
    print(user_id)
    user_engine = get_point_db_engine(user_id)
    db = get_db_session(user_engine)
    try:
        yield db
    finally:
        db.close()

def get_users_db_engine():
    if not USERS_DB_ENGINES.get('users'):
        users_db_engine = create_db_engine(settings.data_base.get_db_url('users'), 5, 10)
        USERS_DB_ENGINES['users'] = users_db_engine
    return USERS_DB_ENGINES.get('users')

def get_users_db():
    users_db_engine = get_users_db_engine()
    db = get_db_session(users_db_engine)
    try:
        yield db
    finally:
        db.close()

def db_safe(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError:
            raise HTTPException(status_code=503, detail="Database is temporarily unavailable")
    return wrapper

# temp
def get_db():
    ...
