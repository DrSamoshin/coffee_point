import logging
from itertools import count
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.db.models import Order, ProductOrder
from app.db.session import db_safe
from app.schemas.order import OrderCreate, OrderUpdate, ShiftOrderOut, OrderStatusUpdate, OrderBase
from app.schemas.product import ProductOrderOut


@db_safe
def create_order_with_products(db: Session, order: OrderCreate):
    try:
        with db.begin():
            db_order = Order(price=order.price,
                             date=order.date,
                             client_id=order.client_id,
                             payment_method=order.payment_method,
                             type=order.type,
                             status=order.status,
                             shift_id=order.shift_id)
            db.add(db_order)
            db.flush()

            for product in order.products:
                db_product_order = ProductOrder(product_id=product.product_id,
                                                order_id=db_order.id,
                                                count=product.count)
                db.add(db_product_order)
        return db_order
    except Exception as e:
        db.rollback()
        raise e

@db_safe
def get_only_order(db: Session, order_id: UUID):
    return db.query(Order).filter(Order.id == order_id).first()

@db_safe
def get_order(db: Session, order_id: UUID):
    order = db.query(Order).filter(Order.id == order_id).options(
        joinedload(Order.product_orders).joinedload(ProductOrder.product)
    ).first()

    order_data = ShiftOrderOut(
                id=order.id,
                date=order.date,
                price=order.price,
                client_id=order.client_id,
                type=order.type,
                status=order.status,
                payment_method=order.payment_method,
                active=order.active,
                products=[ProductOrderOut(
                    id=po.product.id,
                    name=po.product.name,
                    price=po.product.price,
                    image_url=po.product.image_url,
                    product_order_id=po.id,
                    count=po.count,
                    category=po.product.category
                    ) for po in order.product_orders]
            )
    return order_data


@db_safe
def get_orders(db: Session):
    return db.query(Order).filter(Order.active == True).all()

@db_safe
def get_shift_orders(db: Session, shift_id: UUID, skip: int = 0, limit: int = 10):
    orders = db.query(Order).filter(Order.active == True, Order.shift_id == shift_id).options(
        joinedload(Order.product_orders).joinedload(ProductOrder.product)
    ).offset(skip).limit(limit).all()
    logging.info(orders)
    result = []

    for order in orders:

        order_data = ShiftOrderOut(
            id=order.id,
            date=order.date,
            price=order.price,
            client_id=order.client_id,
            type=order.type,
            status=order.status,
            payment_method=order.payment_method,
            active=order.active,
            products=[ProductOrderOut(
                id=po.product.id,
                name=po.product.name,
                price=po.product.price,
                image_url=po.product.image_url,
                product_order_id=po.id,
                count=po.count,
                category=po.product.category
                ) for po in order.product_orders]
        )

        result.append(order_data)

    return result

@db_safe
def get_deactivated_orders(db: Session):
    return db.query(Order).filter(Order.active == False).all()

@db_safe
def update_order_status(db: Session, db_order: OrderBase, updates: OrderStatusUpdate):
    db_order.status = updates.status
    db.commit()
    db.refresh(db_order)
    return db_order

@db_safe
def update_order(db: Session, order_id: UUID, updates: OrderUpdate):
    try:
        with db.begin():
            db_order = db.query(Order).filter(Order.id == order_id).first()
            db_order.price = updates.price
            db_order.date = updates.date
            db_order.payment_method = updates.payment_method
            db_order.type = updates.type
            db_order.client_id = updates.client_id
            db.add(db_order)
            db.flush()

            for product in updates.products:
                if product_order_id:= product.product_order_id:
                    product_order = db.query(ProductOrder).filter(ProductOrder.id == product_order_id).first()
                    if product_order and product.count < 1:
                        db.delete(product_order)
                    elif product_order:
                        product_order.count = product.count
                else:
                    db_product_order = ProductOrder(product_id=product.product_id,
                                                    order_id=db_order.id,
                                                    count=product.count)
                    db.add(db_product_order)
        print(db_order)
        return db_order
    except Exception as e:
        db.rollback()
        raise e

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
