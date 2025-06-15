import logging
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Category
from app.db.session import db_safe
from app.schemas.category import CategoryCreate, CategoryUpdate

@db_safe
def get_category(db: Session, category_id: UUID):
    return db.query(Category).filter(Category.id == category_id).first()

# +
@db_safe
def get_categories(db: Session):
    return db.query(Category).filter(Category.active == True).order_by(Category.name).all()

@db_safe
def get_deactivated_categories(db: Session):
    return db.query(Category).filter(Category.active == False).all()

# +
@db_safe
def create_category(db: Session, category: CategoryCreate):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    logging.info(f"Category is created: {db_category}")
    return db_category

# +
@db_safe
def update_category(db: Session, category_id: UUID, updates: CategoryUpdate):
    try:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        db_category.name = updates.name
        db.commit()
        db.refresh(db_category)
        logging.info(f"Category is updated: {db_category}")
        return db_category
    except Exception as error:
        logging.warning(error)


@db_safe
def delete_category(db: Session, category_id: UUID):
    try:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        db_category.active = False
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as error:
        logging.warning(error)


@db_safe
def activate_category(db: Session, category_id: UUID):
    db_category = db.query(Category).filter(Category.id == category_id, Category.active == False).first()
    if db_category:
        db_category.active = True
        db.commit()
        db.refresh(db_category)
    return db_category
