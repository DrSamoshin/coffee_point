import logging
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Category
from app.db.session import db_safe
from app.schemas.category import CategoryCreate, CategoryUpdate


@db_safe
def get_categories(db: Session):
    logging.info(f"call method get_categories")
    try:
        db_categories = db.query(Category).filter(Category.active == True).order_by(Category.name).all()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"categories: {len(db_categories)}")
        return db_categories

@db_safe
def create_category(db: Session, category: CategoryCreate):
    logging.info(f"call method create_category")
    try:
        db_category = db.query(Category).filter(Category.name == category.name).first()
        if not db_category:
            db_category = Category(name=category.name)
            db.add(db_category)
            db.commit()
            db.refresh(db_category)
        elif not db_category.active:
            db_category.active = True
            db.commit()
            db.refresh(db_category)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"category is created: {db_category}")
        return db_category

@db_safe
def update_category(db: Session, category_id: UUID, updates: CategoryUpdate):
    logging.info(f"call method update_category")
    try:
        db_category = db.query(Category).filter(Category.id == category_id, Category.active == True).first()
        db_category.name = updates.name
        db.commit()
        db.refresh(db_category)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"category is updated: {db_category}")
        return db_category

@db_safe
def delete_category(db: Session, category_id: UUID):
    logging.info(f"call method delete_category")
    try:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        db_category.active = False
        db.commit()
        db.refresh(db_category)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"category is deleted: {db_category}")
        return db_category
