from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.db_sessions import get_point_db
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate, ProductFullInfoOut
from app.crud import product as crud_product
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/products', tags=['products'])

@router.get("/", response_model=list[ProductOut])
async def get_products(db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_products = crud_product.get_products(db)
    return db_products

@router.get("/online-shop/", response_model=list[ProductOut])
async def get_online_shop_products(db: Session = Depends(get_point_db)):
    db_products = crud_product.get_online_shop_products(db)
    return db_products

@router.post("/", response_model=ProductOut)
async def create_product(product: ProductCreate, db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_product = crud_product.create_product(db, product)
    return db_product

@router.put("/{product_id}/", response_model=ProductOut)
async def update_product(product_id: UUID, product_update: ProductUpdate, db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_product = crud_product.update_product(db, product_id, product_update)
    return db_product

@router.delete("/{product_id}/", response_model=ProductFullInfoOut)
async def deactivate_product(product_id: UUID, db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_product = crud_product.delete_product(db, product_id)
    return db_product
