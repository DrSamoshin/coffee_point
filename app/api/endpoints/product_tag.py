from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.product_tag import ProductTagCreate, ProductTagOut, ProductTagUpdate
from app.crud import product_tag as crud_product_tag
from app.core.responses import response

router = APIRouter(prefix='/product_tags', tags=['product_tags'])

@router.get("/", response_model=list[ProductTagOut])
def read_product_tags(db: Session = Depends(get_db)):
    return crud_product_tag.get_product_tags(db)

@router.get("/{product_tag_id}", response_model=ProductTagOut)
def read_product_tag(product_tag_id: UUID, db: Session = Depends(get_db)):
    db_product_tag = crud_product_tag.get_product_tag(db, product_tag_id)
    if not db_product_tag:
        return response("product_tag not found", 404)
    return db_product_tag

@router.post("/", response_model=ProductTagOut)
def create_product_tag(product_tag: ProductTagCreate, db: Session = Depends(get_db)):
    db_product_tag = crud_product_tag.create_product_tag(db, product_tag)
    return db_product_tag

@router.put("/{product_tag_id}", response_model=ProductTagOut)
def update_product_tag(product_tag_id: UUID, product_tag_update: ProductTagUpdate, db: Session = Depends(get_db)):
    db_product_tag = crud_product_tag.get_product_tag(db, product_tag_id)
    if not db_product_tag:
        return response("product_tag not found", 404)
    db_product_tag = crud_product_tag.update_product_tag(db, db_product_tag, product_tag_update)
    return db_product_tag
