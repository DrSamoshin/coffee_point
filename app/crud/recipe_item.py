import logging
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models import RecipeItem
from app.db.db_sessions import db_safe
from app.schemas.recipe_item import RecipeItemCreate, RecipeItemUpdate


@db_safe
def get_recipe_item(db: Session, recipe_item_id: UUID):
    logging.info("call method get_recipe_item")
    try:
        recipe_item = (
            db.query(RecipeItem).filter(RecipeItem.id == recipe_item_id).first()
        )
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"recipe_item: {recipe_item}")
        return recipe_item


@db_safe
def get_recipe_items(db: Session):
    logging.info("call method get_recipe_items")
    try:
        recipe_items = db.query(RecipeItem).all()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"recipe_items: {len(recipe_items)}")
        return recipe_items


@db_safe
def create_recipe_item(db: Session, recipe_item: RecipeItemCreate):
    logging.info("call method create_recipe_item")
    try:
        db_recipe_item = RecipeItem(
            product_id=recipe_item.product_id,
            item_id=recipe_item.item_id,
            amount=recipe_item.amount,
        )
        db.add(db_recipe_item)
        db.commit()
        db.refresh(db_recipe_item)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"recipe_item is created: {db_recipe_item}")
        return db_recipe_item


@db_safe
def update_recipe_item(db: Session, recipe_item_id: UUID, updates: RecipeItemUpdate):
    logging.info("call method update_recipe_item")
    try:
        db_recipe_item = (
            db.query(RecipeItem).filter(RecipeItem.id == recipe_item_id).first()
        )
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_recipe_item, field, value)
        db.commit()
        db.refresh(db_recipe_item)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"recipe_item is updated: {db_recipe_item}")
        return db_recipe_item
