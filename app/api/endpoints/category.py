from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate
from app.crud import category as crud_category
from app.core.responses import response

router = APIRouter(prefix='/categories', tags=['categories'])

@router.get("/", response_model=list[CategoryOut])
def read_categories(db: Session = Depends(get_db)):
    return crud_category.get_categories(db)

@router.get("/{category_id}", response_model=CategoryOut)
def read_category(category_id: UUID, db: Session = Depends(get_db)):
    db_category = crud_category.get_category(db, category_id)
    if not db_category:
        return response("category not found", 404)
    return db_category

@router.post("/", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = crud_category.create_category(db, category)
    return db_category

@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: UUID, category_update: CategoryUpdate, db: Session = Depends(get_db)):
    db_category = crud_category.get_category(db, category_id)
    if not db_category:
        return response("category not found", 404)
    db_category = crud_category.update_category(db, db_category, category_update)
    return db_category
