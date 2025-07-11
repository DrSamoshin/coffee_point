from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.db_sessions import get_point_db
from app.schemas.order import OrderCreate, OrderOut, OrderUpdate, ShiftOrderOut, OrderStatusUpdate
from app.crud import order as crud_order
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/orders', tags=['orders'])

@router.get("/shift-orders/", response_model=list[ShiftOrderOut])
async def get_shift_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_point_db)):
    db_orders = crud_order.get_active_shift_orders(db, skip, limit)
    return db_orders

@router.get("/waiting-shift-orders/", response_model=list[ShiftOrderOut])
async def get_shift_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_point_db)):
    db_orders = crud_order.get_waiting_shift_orders(db, skip, limit)
    return db_orders

@router.get("/{order_id}/", response_model=ShiftOrderOut)
async def get_order(order_id: UUID, db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_order = crud_order.get_order(db, order_id)
    return db_order

@router.post("/", response_model=OrderOut)
async def create_order_with_products(order: OrderCreate, db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_order = crud_order.create_order_with_products(db, order)
    return db_order

@router.put("/{order_id}/", response_model=OrderOut)
async def update_order(order_id: UUID, order_update: OrderUpdate, db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_order = crud_order.update_order(db, order_id, order_update)
    return db_order

@router.put("/status-update/{order_id}/", response_model=OrderOut)
async def update_order_status(order_id: UUID, status_update: OrderStatusUpdate, db: Session = Depends(get_point_db), user_id: str = Depends(get_user_id_from_token)):
    db_order = crud_order.update_order_status(db, order_id, status_update)
    return db_order
