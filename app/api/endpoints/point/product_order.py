from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.db_sessions import get_point_db
from app.schemas.product_order import ProductOrderCreate, ProductOrderOut, ProductOrderUpdate
from app.crud import product_order as crud_product_order
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/product-orders', tags=['product_orders'])

@router.get("/", response_model=list[ProductOrderOut])
async def read_product_orders(db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_product_orders = crud_product_order.get_product_orders(db)
    return db_product_orders

@router.get("/{product_order_id}/", response_model=ProductOrderOut)
async def read_product_order(product_order_id: UUID, db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_product_order = crud_product_order.get_product_order(db, product_order_id)
    return db_product_order

@router.post("/", response_model=ProductOrderOut)
async def create_product_order(product_order: ProductOrderCreate, db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_product_order = crud_product_order.create_product_order(db, product_order)
    return db_product_order

@router.put("/{product_order_id}/", response_model=ProductOrderOut)
async def update_product_order(product_order_id: UUID, product_order_update: ProductOrderUpdate, db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_product_order = crud_product_order.update_product_order(db, product_order_id, product_order_update)
    return db_product_order
