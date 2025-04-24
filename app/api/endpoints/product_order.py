from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.product_order import ProductOrderCreate, ProductOrderOut, ProductOrderUpdate
from app.crud import product_order as crud_product_order
from app.core.responses import response

router = APIRouter(prefix='/product_orders', tags=['product_orders'])

@router.get("/", response_model=list[ProductOrderOut])
def read_product_orders(db: Session = Depends(get_db)):
    return crud_product_order.get_product_orders(db)

@router.get("/{product_order_id}", response_model=ProductOrderOut)
def read_product_order(product_order_id: UUID, db: Session = Depends(get_db)):
    db_product_order = crud_product_order.get_product_order(db, product_order_id)
    if not db_product_order:
        return response("product_order not found", 404)
    return db_product_order

@router.post("/", response_model=ProductOrderOut)
def create_product_order(product_order: ProductOrderCreate, db: Session = Depends(get_db)):
    db_product_order = crud_product_order.create_product_order(db, product_order)
    return db_product_order

@router.put("/{product_order_id}", response_model=ProductOrderOut)
def update_product_order(product_order_id: UUID, product_order_update: ProductOrderUpdate, db: Session = Depends(get_db)):
    db_product_order = crud_product_order.get_product_order(db, product_order_id)
    if not db_product_order:
        return response("product_order not found", 404)
    db_product_order = crud_product_order.update_product_order(db, db_product_order, product_order_update)
    return db_product_order
