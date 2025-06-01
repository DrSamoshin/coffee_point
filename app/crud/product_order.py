from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.db.models import ProductOrder
from app.db.session import db_safe
from app.schemas.product_order import ProductOrderCreate, ProductOrderUpdate

@db_safe
def get_product_order(db: Session, product_order_id: UUID):
    return db.query(ProductOrder).filter(ProductOrder.id == product_order_id).first()

@db_safe
def get_product_orders(db: Session):
    return db.query(ProductOrder).all()


@db_safe
def get_product_with_orders(db: Session):
    return db.query(ProductOrder).options(
        joinedload(ProductOrder.product),
        joinedload(ProductOrder.order)
    ).all()


@db_safe
def create_product_order(db: Session, product_order: ProductOrderCreate):
    db_product_order = ProductOrder(product_id=product_order.product_id,
                                    order_id=product_order.order_id,
                                    count=product_order.count)
    db.add(db_product_order)
    db.commit()
    db.refresh(db_product_order)
    return db_product_order

@db_safe
def update_product_order(db: Session, db_product_order: ProductOrder, updates: ProductOrderUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_product_order, field, value)
    db.commit()
    db.refresh(db_product_order)
    return db_product_order

@db_safe
def delete_product_order(db: Session, db_product_order: ProductOrder):
    db.delete(db_product_order)
    db.commit()