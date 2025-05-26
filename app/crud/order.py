import logging
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.db.models import Order, ProductOrder
from app.db.session import db_safe
from app.schemas.order import OrderCreate, OrderUpdate, OrderWithProductsOut
from app.schemas.product import ProductOut


@db_safe
def get_order(db: Session, order_id: UUID):
    return db.query(Order).filter(Order.id == order_id).first()

@db_safe
def get_all_orders(db: Session):
    return db.query(Order).filter(Order.active == True).all()

@db_safe
def get_orders_by_shift_id(db: Session, shift_id: UUID):
    orders = db.query(Order).filter(Order.active == True, Order.shift_id == shift_id).options(
        joinedload(Order.product_orders).joinedload(ProductOrder.product)
    ).all()

    result = []

    for order in orders:

        products = [ProductOut.model_validate(po.product) for po in order.product_orders]
        logging.info(products)
        order_data = OrderWithProductsOut(
            id=order.id,
            date=order.date,
            price=order.price,
            shift_id=order.shift_id,
            client_id=order.client_id,
            type=order.type,
            payment_method=order.payment_method,
            active=order.active,
            products=products
        )

        result.append(order_data)

    return result

@db_safe
def get_deactivated_orders(db: Session):
    return db.query(Order).filter(Order.active == False).all()

@db_safe
def create_order(db: Session, order: OrderCreate):
    db_order = Order(price=order.price,
                     date=order.date,
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
