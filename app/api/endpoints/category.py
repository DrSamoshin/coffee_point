from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate
from app.crud import category as crud_category
from app.core.responses import response
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/categories', tags=['categories'])

# barista_app
@router.get("/", response_model=list[CategoryOut])
async def get_categories(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    return crud_category.get_categories(db)

# @router.get("/{category_id}/", response_model=CategoryOut)
# async def get_category(category_id: UUID, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
#     db_category = crud_category.get_category(db, category_id)
#     if not db_category:
#         return response("category not found", 404)
#     return db_category

# barista_app
@router.post("/", response_model=CategoryOut)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_category = crud_category.create_category(db, category)
    return db_category

# barista_app
@router.put("/{category_id}/", response_model=CategoryOut)
async def update_category(category_id: UUID, category_update: CategoryUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_category = crud_category.get_category(db, category_id)
    if not db_category:
        return response("category not found", 404)
    db_category = crud_category.update_category(db, db_category, category_update)
    return db_category
