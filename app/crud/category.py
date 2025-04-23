from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

def get_category(db: Session, category_id: UUID):
    return db.query(Category).filter(Category.id == category_id).first()

def get_categories(db: Session):
    return db.query(Category).filter(Category.active == True).all()

def get_deactivated_categories(db: Session):
    return db.query(Category).filter(Category.active == False).all()

def create_category(db: Session, category: CategoryCreate):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, db_category: Category, updates: CategoryUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_category, field, value)
    db.commit()
    db.refresh(db_category)
    return db_category

def deactivate_category(db: Session, db_category: Category):
    db_category.active = False
    db.commit()
    db.refresh(db_category)

def activate_category(db: Session, category_id: UUID):
    db_category = db.query(Category).filter(Category.id == category_id, Category.active == False).first()
    if db_category:
        db_category.active = True
        db.commit()
        db.refresh(db_category)
    return db_category
