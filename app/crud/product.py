from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Product
from app.schemas.product import ProductCreate, ProductUpdate

def get_product(db: Session, product_id: UUID):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session):
    return db.query(Product).filter(Product.active == True).all()

def get_deactivated_products(db: Session):
    return db.query(Product).filter(Product.active == False).all()

def create_product(db: Session, product: ProductCreate):
    db_product = Product(name=product.name,
                         category_id=product.category_id,
                         price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, db_product: Product, updates: ProductUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_product, field, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def deactivate_product(db: Session, db_product: Product):
    db_product.active = False
    db.commit()
    db.refresh(db_product)

def activate_product(db: Session, category_id: UUID):
    db_product = db.query(Product).filter(Product.id == category_id, Product.active == False).first()
    if db_product:
        db_product.active = True
        db.commit()
        db.refresh(db_product)
    return db_product
