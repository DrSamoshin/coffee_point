from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import RecipeItem
from app.schemas.recipe_item import RecipeItemCreate, RecipeItemUpdate

def get_recipe_item(db: Session, recipe_item_id: UUID):
    return db.query(RecipeItem).filter(RecipeItem.id == recipe_item_id).first()

def get_recipe_items(db: Session):
    return db.query(RecipeItem).all()

def create_recipe_item(db: Session, recipe_item: RecipeItemCreate):
    db_recipe_item = RecipeItem(product_id=recipe_item.product_id,
                                item_id=recipe_item.item_id,
                                amount=recipe_item.amount)
    db.add(db_recipe_item)
    db.commit()
    db.refresh(db_recipe_item)
    return db_recipe_item

def update_recipe_item(db: Session, db_recipe_item: RecipeItem, updates: RecipeItemUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_recipe_item, field, value)
    db.commit()
    db.refresh(db_recipe_item)
    return db_recipe_item

def delete_recipe_item(db: Session, db_recipe_item: RecipeItem):
    db.delete(db_recipe_item)
    db.commit()