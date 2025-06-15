import logging
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.db.models import Order, ProductOrder
from app.db.session import db_safe
from app.schemas.order import OrderCreate, OrderUpdate, ShiftOrderOut, OrderStatusUpdate, OrderBase
from app.schemas.product import ProductOrderOut
from app.core.consts import OrderStatus


@db_safe
def create_order_with_products(db: Session, order: OrderCreate):
    logging.info(f"call method create_order_with_products")
    try:
        with db.begin():
            last_order_number =  db.query(func.max(Order.order_number)).filter(Order.shift_id == order.shift_id).scalar()
            db_order = Order(price=order.price,
                             discount=order.discount,
                             date=datetime.now(timezone.utc),
                             client_id=order.client_id,
                             payment_method=order.payment_method,
                             type=order.type,
                             status=order.status,
                             shift_id=order.shift_id,
                             order_number=(last_order_number or 0) + 1)
            db.add(db_order)
            db.flush()

            if order.products:
                for product in order.products:
                    db_product_order = ProductOrder(product_id=product.product_id,
                                                    order_id=db_order.id,
                                                    count=product.count)
                    db.add(db_product_order)
        db.refresh(db_order)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"order is created: {db_order}")
        return db_order

@db_safe
def get_order(db: Session, order_id: UUID):
    logging.info(f"call method get_order")
    try:
        order = db.query(Order).filter(Order.id == order_id).options(
            joinedload(Order.product_orders).joinedload(ProductOrder.product)
        ).first()

        order_data = ShiftOrderOut(
                    id=order.id,
                    date=order.date,
                    price=order.price,
                    discount=order.discount,
                    client_id=order.client_id,
                    type=order.type,
                    status=order.status,
                    payment_method=order.payment_method,
                    active=order.active,
                    order_number=order.order_number,
                    products=[ProductOrderOut(
                        product_order_id=po.id,
                        count=po.count,
                        product_id=po.product.id,
                        product_name=po.product.name,
                        product_price=po.product.price
                        ) for po in order.product_orders]
                )
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"order: {order_data}")
        return order_data

@db_safe
def get_shift_orders(db: Session, shift_id: UUID, skip: int = 0, limit: int = 10):
    logging.info(f"call method get_shift_orders")
    try:
        orders = (db.query(Order)
                  .filter(Order.active == True, Order.shift_id == shift_id)
                  .options(joinedload(Order.product_orders).joinedload(ProductOrder.product))
                  .order_by(desc(Order.date))
                  .offset(skip)
                  .limit(limit)
                  .all())
        shift_orders = []
        for order in orders:
            order_data = ShiftOrderOut(
                id=order.id,
                date=order.date,
                price=order.price,
                discount=order.discount,
                client_id=order.client_id,
                type=order.type,
                status=order.status,
                payment_method=order.payment_method,
                active=order.active,
                order_number=order.order_number,
                products=[ProductOrderOut(
                    product_order_id=po.id,
                    count=po.count,
                    product_id=po.product.id,
                    product_name=po.product.name,
                    product_price=po.product.price
                    ) for po in order.product_orders]
            )
            shift_orders.append(order_data)
    except Exception as error:
            logging.error(error)
    else:
        logging.info(f"orders: {len(shift_orders)}")
        return shift_orders

@db_safe
def get_waiting_shift_orders(db: Session, shift_id: UUID, skip: int = 0, limit: int = 10):
    logging.info(f"call method get_waiting_shift_orders")
    try:
        orders = (db.query(Order)
                  .filter(Order.active == True, Order.shift_id == shift_id, Order.status == OrderStatus.waiting)
                  .options(joinedload(Order.product_orders).joinedload(ProductOrder.product))
                  .order_by(desc(Order.date))
                  .offset(skip)
                  .limit(limit)
                  .all())
        shift_orders = []
        for order in orders:
            order_data = ShiftOrderOut(
                id=order.id,
                date=order.date,
                price=order.price,
                discount=order.discount,
                client_id=order.client_id,
                type=order.type,
                status=order.status,
                payment_method=order.payment_method,
                active=order.active,
                order_number=order.order_number,
                products=[ProductOrderOut(
                    product_order_id=po.id,
                    count=po.count,
                    product_id=po.product.id,
                    product_name=po.product.name,
                    product_price=po.product.price
                    ) for po in order.product_orders]
            )
            shift_orders.append(order_data)
    except Exception as error:
            logging.error(error)
    else:
        logging.info(f"orders: {len(shift_orders)}")
        return shift_orders

@db_safe
def update_order_status(db: Session, order_id: UUID, updates: OrderStatusUpdate):
    logging.info(f"call method update_order_status")
    try:
        db_order = db.query(Order).filter(Order.id == order_id).first()
        db_order.status = updates.status
        db.commit()
        db.refresh(db_order)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"order status is updated: {db_order}")
        return db_order

@db_safe
def update_order(db: Session, order_id: UUID, updates: OrderUpdate):
    logging.info(f"call method update_order")
    try:
        with db.begin():
            db_order = db.query(Order).filter(Order.id == order_id).first()
            for field, value in updates.model_dump(exclude_unset=True).items():
                setattr(db_order, field, value)
            db.add(db_order)
            db.flush()

            if updates.products:
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
        db.refresh(db_order)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"order is updated: {db_order}")
        return db_order

