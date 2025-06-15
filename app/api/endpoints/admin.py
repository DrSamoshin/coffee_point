from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from run import run_alembic_upgrade
from app.core.responses import response
from app.db.session import get_db
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/reset-db/")
def reset_database(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db.execute(text("DROP SCHEMA public CASCADE"))
    db.execute(text("CREATE SCHEMA public"))
    db.commit()
    run_alembic_upgrade()
    return response("db is cleaned", 200, "success")