from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.configs import settings


engine = create_engine(settings.data_base.sqlalchemy_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
