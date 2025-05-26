from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderOut, OrderUpdate, OrderWithProductsOut
from app.crud import order as crud_order
from app.core.responses import response
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/orders', tags=['orders'])

@router.get("/", response_model=list[OrderOut])
async def read_orders(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    return crud_order.get_all_orders(db)

@router.get("/shift-orders-with-products/{shift_id}/", response_model=list[OrderWithProductsOut])
async def get_orders_with_products(shift_id: UUID, db: Session = Depends(get_db)):
    return crud_order.get_orders_by_shift_id(db, shift_id)

@router.get("/{order_id}/", response_model=OrderOut)
async def read_order(order_id: UUID, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_order = crud_order.get_order(db, order_id)
    if not db_order:
        return response("order not found", 404, "error")
    return db_order

@router.post("/", response_model=OrderOut)
async def create_order(order: OrderCreate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_order = crud_order.create_order(db, order)
    return db_order

@router.put("/{order_id}/", response_model=OrderOut)
async def update_order(order_id: UUID, order_update: OrderUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_order = crud_order.get_order(db, order_id)
    if not db_order:
        return response("order not found", 404, "error")
    db_order = crud_order.update_order(db, db_order, order_update)
    return db_order
