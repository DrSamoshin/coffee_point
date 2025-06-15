import logging
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.db.models import Product
from app.db.session import db_safe
from app.schemas.product import ProductCreate, ProductUpdate


@db_safe
def get_products(db: Session):
    logging.info(f"call method create_item")
    return db.query(Product).filter(Product.active == True).options(
        joinedload(Product.category)
    ).all()

@db_safe
def get_online_shop_products(db: Session):
    logging.info(f"call method create_item")
    return db.query(Product).filter(Product.active == True, Product.online_shop == True).options(
        joinedload(Product.category)
    ).all()

@db_safe
def create_product(db: Session, product: ProductCreate):
    logging.info(f"call method create_item")
    db_product = Product(name=product.name,
                         category_id=product.category_id,
                         price=product.price,
                         online_shop=product.online_shop,
                         image_url=product.image_url)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@db_safe
def update_product(db: Session, product_id: UUID, updates: ProductUpdate):
    try:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as error:
        logging.warning(error)

@db_safe
def deactivate_product(db: Session, product_id: UUID):
    try:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        db_product.active = False
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as error:
        logging.warning(error)

@db_safe
def activate_product(db: Session, category_id: UUID):
    db_product = db.query(Product).filter(Product.id == category_id, Product.active == False).first()
    if db_product:
        db_product.active = True
        db.commit()
        db.refresh(db_product)
    return db_product
