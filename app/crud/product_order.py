from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import ProductOrder
from app.schemas.product_order import ProductOrderCreate, ProductOrderUpdate

def get_product_order(db: Session, product_order_id: UUID):
    return db.query(ProductOrder).filter(ProductOrder.id == product_order_id).first()

def get_product_orders(db: Session):
    return db.query(ProductOrder).all()

def create_product_order(db: Session, product_order: ProductOrderCreate):
    db_product_order = ProductOrder(product_id=product_order.product_id,
                                    order_id=product_order.order_id)
    db.add(db_product_order)
    db.commit()
    db.refresh(db_product_order)
    return db_product_order

def update_product_order(db: Session, db_product_order: ProductOrder, updates: ProductOrderUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_product_order, field, value)
    db.commit()
    db.refresh(db_product_order)
    return db_product_order

def delete_product_order(db: Session, db_product_order: ProductOrder):
    db.delete(db_product_order)
    db.commit()