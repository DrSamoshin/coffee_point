from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Order
from app.db.session import db_safe
from app.schemas.order import OrderCreate, OrderUpdate

@db_safe
def get_order(db: Session, order_id: UUID):
    return db.query(Order).filter(Order.id == order_id).first()

@db_safe
def get_orders(db: Session):
    return db.query(Order).filter(Order.active == True).all()

@db_safe
def get_deactivated_orders(db: Session):
    return db.query(Order).filter(Order.active == False).all()

@db_safe
def create_order(db: Session, order: OrderCreate):
    db_order = Order(price=order.price,
                     date=order.price,
                     client_id=order.client_id,
                     payment_method=order.payment_method,
                     type=order.type,
                     shift_id=order.shift_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@db_safe
def update_order(db: Session, db_order: Order, updates: OrderUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_order, field, value)
    db.commit()
    db.refresh(db_order)
    return db_order

@db_safe
def deactivate_order(db: Session, db_order: Order):
    db_order.active = False
    db.commit()
    db.refresh(db_order)

@db_safe
def activate_order(db: Session, order_id: UUID):
    db_order = db.query(Order).filter(Order.id == order_id, Order.active == False).first()
    if db_order:
        db_order.active = True
        db.commit()
        db.refresh(db_order)
    return db_order
