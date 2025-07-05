import logging
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.db.models import ProductOrder
from app.db.db_sessions import db_safe
from app.schemas.product_order import ProductOrderCreate, ProductOrderUpdate

@db_safe
def get_product_order(db: Session, product_order_id: UUID):
    logging.info(f"call method get_product_order")
    try:
        db_product_order = db.query(ProductOrder).filter(ProductOrder.id == product_order_id).first()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"product_order: {db_product_order}")
        return db_product_order

@db_safe
def get_product_orders(db: Session):
    logging.info(f"call method get_product_orders")
    try:
        db_product_orders = db.query(ProductOrder).all()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"product_orders: {len(db_product_orders)}")
        return db_product_orders

@db_safe
def create_product_order(db: Session, product_order: ProductOrderCreate):
    logging.info(f"call method create_product_order")
    try:
        db_product_order = ProductOrder(product_id=product_order.product_id,
                                        order_id=product_order.order_id,
                                        count=product_order.count)
        db.add(db_product_order)
        db.commit()
        db.refresh(db_product_order)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"product_order is created: {db_product_order}")
        return db_product_order

@db_safe
def update_product_order(db: Session, product_order_id: UUID, updates: ProductOrderUpdate):
    logging.info(f"call method update_product_order")
    try:
        db_product_order = db.query(ProductOrder).filter(ProductOrder.id == product_order_id).first()
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_product_order, field, value)
        db.commit()
        db.refresh(db_product_order)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"product_order is updated: {db_product_order}")
        return db_product_order
