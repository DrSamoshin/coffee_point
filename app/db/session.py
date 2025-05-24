import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.configs import settings
from functools import wraps
from sqlalchemy.exc import OperationalError
from fastapi import HTTPException


engine = create_engine(settings.data_base.sqlalchemy_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_db_availability():
    try:
        engine.connect()
        logging.info(f"DB is available")
    except OperationalError:
        settings.data_base.DB_AVAILABLE = False
        logging.warning(f"DB is not available")

def get_db():
    db = SessionLocal()
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
