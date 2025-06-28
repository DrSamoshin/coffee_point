import logging
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.db.models import Product
from app.db.session import db_safe
from app.schemas.product import ProductCreate, ProductUpdate


@db_safe
def get_products(db: Session):
    logging.info(f"call method get_products")
    try:
        db_products = (db.query(Product)
                       .filter(Product.active == True)
                       .options(joinedload(Product.category))
                       .order_by(Product.name)
                       .all())
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"products: {len(db_products)}")
        return db_products

@db_safe
def get_online_shop_products(db: Session):
    logging.info(f"call method get_online_shop_products")
    try:
        db_products = (db.query(Product)
                       .filter(Product.active == True, Product.online_shop == True)
                       .options(joinedload(Product.category))
                       .all())
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"online_shop_products: {len(db_products)}")
        return db_products

@db_safe
def create_product(db: Session, product: ProductCreate):
    logging.info(f"call method create_product")
    try:
        db_product = db.query(Product).filter(Product.name == product.name).first()
        if not db_product:
            db_product = Product(name=product.name,
                                 category_id=product.category_id,
                                 price=product.price,
                                 online_shop=product.online_shop,
                                 image_url=product.image_url)
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
        else:
            db_product.active = True
            db.commit()
            db.refresh(db_product)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"product is created: {db_product}")
        return db_product

@db_safe
def update_product(db: Session, product_id: UUID, updates: ProductUpdate):
    logging.info(f"call method update_product")
    try:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        for field, value in updates.model_dump().items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"product is updated: {db_product}")
        return db_product

@db_safe
def delete_product(db: Session, product_id: UUID):
    logging.info(f"call method delete_product")
    try:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        db_product.active = False
        db.commit()
        db.refresh(db_product)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"product is deleted: {db_product}")
        return db_product
