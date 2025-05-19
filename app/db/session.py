import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.configs import settings
from functools import wraps
from sqlalchemy.exc import OperationalError
from fastapi import HTTPException


if settings.data_base.DB_AVAILABLE:
    engine = create_engine(settings.data_base.sqlalchemy_url, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    engine = None
    SessionLocal = lambda: None


def get_db():
    if not settings.data_base.DB_AVAILABLE:
        raise HTTPException(status_code=503, detail="Database is temporarily unavailable")
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
