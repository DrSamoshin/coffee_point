from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import subprocess
import os

from app.core.responses import response
from app.db.db_sessions import get_users_db
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/migrate-users-db/")
def migrate_point_db(user_id: UUID = Depends(get_user_id_from_token)):
    try:
        result = subprocess.run(
            ["alembic", "-c", "alembic_users_db/alembic.ini", "upgrade", "head"],
            capture_output=True,
            text=True,
            check=True
        )
        print(result)
        return response("db is migrated", 200, "success")
    except subprocess.CalledProcessError as e:
        return response("db is not migrated", 500, "error")

@router.get("/migrate-point-db/{db_name}/")
def migrate_point_db(db_name: str, user_id: UUID = Depends(get_user_id_from_token)):
    try:
        os.environ["TARGET_DB_NAME"] = db_name
        print(os.environ.get("TARGET_DB_NAME"))
        result = subprocess.run(
            ["alembic", "-c", "alembic_points_db/alembic.ini", "upgrade", "head"],
            capture_output=True,
            text=True,
            check=True
        )
        print(result)
        return response("db is migrated", 200, "success")
    except subprocess.CalledProcessError as e:
        return response("db is not migrated", 500, "error")
