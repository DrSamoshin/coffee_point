import logging
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.consts import OrderStatus
from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderOut, OrderUpdate, ShiftOrderOut, OrderStatusUpdate
from app.crud import order as crud_order
from app.core.responses import response
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/orders', tags=['orders'])

# barista
@router.post("/", response_model=OrderOut)
async def create_order_with_products(order: OrderCreate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_order = crud_order.create_order_with_products(db, order)
    return db_order

# @router.get("/", response_model=list[OrderOut])
# async def get_orders(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
#     return crud_order.get_orders(db)

# barista
@router.get("/shift-orders/{shift_id}/", response_model=list[ShiftOrderOut])
async def get_shift_orders(shift_id: UUID, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_order.get_shift_orders(db, shift_id, skip, limit)

# barista
@router.get("/{order_id}/", response_model=ShiftOrderOut)
async def get_order(order_id: UUID, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_order = crud_order.get_order(db, order_id)
    if not db_order:
        return response("order not found", 404, "error")
    return db_order

# barista
@router.put("/{order_id}/", response_model=OrderOut)
async def update_order(order_id: UUID, order_update: OrderUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    # db_order = crud_order.get_order(db, order_id)
    # logging.info(db_order)
    # if not db_order:
    #     return response("order not found", 404, "error")
    db_order = crud_order.update_order(db, order_id, order_update)
    logging.info(db_order)
    return db_order

# barista
@router.put("/status-update/{order_id}/", response_model=OrderOut)
async def update_order_status(order_id: UUID, status_update: OrderStatusUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_order = crud_order.get_only_order(db, order_id)
    logging.info(db_order)
    if not db_order:
        return response("order not found", 404, "error")
    db_order = crud_order.update_order_status(db, db_order, status_update)
    logging.info(db_order)
    return db_order
