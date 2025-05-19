from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import ProductTag
from app.db.session import db_safe
from app.schemas.product_tag import ProductTagCreate, ProductTagUpdate

@db_safe
def get_product_tag(db: Session, product_tag_id: UUID):
    return db.query(ProductTag).filter(ProductTag.id == product_tag_id).first()

@db_safe
def get_product_tags(db: Session):
    return db.query(ProductTag).all()

@db_safe
def create_product_tag(db: Session, product_tag: ProductTagCreate):
    db_product_tag = ProductTag(product_id=product_tag.product_id,
                                order_id=product_tag.tag_id)
    db.add(db_product_tag)
    db.commit()
    db.refresh(db_product_tag)
    return db_product_tag

@db_safe
def update_product_tag(db: Session, db_product_tag: ProductTag, updates: ProductTagUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_product_tag, field, value)
    db.commit()
    db.refresh(db_product_tag)
    return db_product_tag

@db_safe
def delete_product_tag(db: Session, db_product_tag: ProductTag):
    db.delete(db_product_tag)
    db.commit()