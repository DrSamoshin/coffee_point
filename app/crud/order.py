from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Order
from app.schemas.order import OrderCreate, OrderUpdate

def get_order(db: Session, order_id: UUID):
    return db.query(Order).filter(Order.id == order_id).first()

def get_orders(db: Session):
    return db.query(Order).filter(Order.active == True).all()

def get_deactivated_orders(db: Session):
    return db.query(Order).filter(Order.active == False).all()

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

def update_order(db: Session, db_order: Order, updates: OrderUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_order, field, value)
    db.commit()
    db.refresh(db_order)
    return db_order

def deactivate_order(db: Session, db_order: Order):
    db_order.active = False
    db.commit()
    db.refresh(db_order)


def activate_order(db: Session, order_id: UUID):
    db_order = db.query(Order).filter(Order.id == order_id, Order.active == False).first()
    if db_order:
        db_order.active = True
        db.commit()
        db.refresh(db_order)
    return db_order
