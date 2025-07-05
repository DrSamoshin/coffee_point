import logging
from uuid import UUID
from functools import wraps
from fastapi import HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from cachetools import TTLCache
from threading import Lock

from app.crud import user as crud_user
from app.core.configs import settings
from app.services.authentication import get_user_id_from_token

USERS_DB_ENGINES = TTLCache(maxsize=10, ttl=3600)
POINT_DB_ENGINES = TTLCache(maxsize=100, ttl=3600)
POINT_URLS = TTLCache(maxsize=100, ttl=3600)

point_engine_lock = Lock()
user_engine_lock = Lock()


def _create_db_engine(url: str, pool_size: int = 3, max_overflow: int = 1):
    try:
        db_engine = create_engine(
            url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=30,
            pool_recycle=1800,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 5}
        )
        db_engine.connect()
    except Exception as error:
        logging.error(f"db engine error: {error}, db_url: {url}")
        raise HTTPException(status_code=503, detail="Database temporarily unavailable")
    else:
        return db_engine

def _get_db_session(user_db_engine):
    try:
        session = sessionmaker(autocommit=False, autoflush=False, bind=user_db_engine)
    except Exception as error:
        logging.error(f"session engine error: {error}")
    else:
        return session()

def check_users_db_availability():
    try:
        users_db_engine = _get_users_db_engine()
        users_db_engine.connect()
        logging.info(f"users DB is available")
    except OperationalError as error:
        settings.data_base.DB_AVAILABLE = False
        logging.info(error)
        logging.warning(f"users DB is not available")

def _get_point_db_url(user_id: UUID):
    with point_engine_lock:
        if not POINT_URLS.get(user_id):
            users_db_engine = _get_users_db_engine()
            db = _get_db_session(users_db_engine)
            db_user = crud_user.get_user(db=db, user_id=user_id)
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            user_db_name = db_user.db_name
            user_db_url = settings.data_base.get_db_url(user_db_name)
            POINT_URLS[user_id] = user_db_url
        return POINT_URLS.get(user_id)

def _get_point_db_engine(user_id: UUID):
    with point_engine_lock:
        if not POINT_DB_ENGINES.get(user_id):
            user_db_url = _get_point_db_url(user_id)
            user_engine = _create_db_engine(user_db_url)
            POINT_DB_ENGINES[user_id] = user_engine
        return POINT_DB_ENGINES.get(user_id)

def _get_users_db_engine():
    with user_engine_lock:
        if not USERS_DB_ENGINES.get('users'):
            users_db_engine = _create_db_engine(settings.data_base.get_db_url('users'), 5, 10)
            USERS_DB_ENGINES['users'] = users_db_engine
        return USERS_DB_ENGINES.get('users')

def get_point_db(user_id: UUID = Depends(get_user_id_from_token)):
    logging.info(f"call method get_point_db")
    user_engine = _get_point_db_engine(user_id)
    logging.info(f"POINT_DB_ENGINES: {len(POINT_DB_ENGINES)}")
    db = _get_db_session(user_engine)
    try:
        yield db
    finally:
        db.close()

def get_users_db():
    logging.info(f"call method get_users_db")
    users_db_engine = _get_users_db_engine()
    logging.info(f"USERS_DB_ENGINES: {len(USERS_DB_ENGINES)}")
    db = _get_db_session(users_db_engine)
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
