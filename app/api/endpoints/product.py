from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.crud import product as crud_product
from app.core.responses import response
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/products', tags=['products'])

# barista
@router.post("/", response_model=ProductOut)
async def create_product(product: ProductCreate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_product = crud_product.create_product(db, product)
    return db_product

# barista
@router.get("/", response_model=list[ProductOut])
async def get_products(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    return crud_product.get_products(db)

# web_page
@router.get("/online-shop/", response_model=list[ProductOut])
async def get_online_shop_products(db: Session = Depends(get_db)):
    return crud_product.get_online_shop_products(db)

# @router.get("/{product_id}/", response_model=ProductOut)
# async def read_product(product_id: UUID, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
#     db_product = crud_product.get_product(db, product_id)
#     if not db_product:
#         return response("product not found", 404)
#     return db_product

# barista
@router.put("/{product_id}/", response_model=ProductOut)
async def update_product(product_id: UUID, product_update: ProductUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_product = crud_product.get_product(db, product_id)
    if not db_product:
        return response("product not found", 404)
    db_product = crud_product.update_product(db, db_product, product_update)
    return db_product
