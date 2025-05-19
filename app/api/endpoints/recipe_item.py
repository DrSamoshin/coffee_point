from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.recipe_item import RecipeItemCreate, RecipeItemOut, RecipeItemUpdate
from app.crud import recipe_item as crud_recipe_item
from app.core.responses import response
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/recipe_items', tags=['recipe_items'])

@router.get("/", response_model=list[RecipeItemOut])
async def read_recipe_items(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    return crud_recipe_item.get_recipe_items(db)

@router.get("/{recipe_item_id}/", response_model=RecipeItemOut)
async def read_recipe_item(recipe_item_id: UUID, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_recipe_item = crud_recipe_item.get_recipe_item(db, recipe_item_id)
    if not db_recipe_item:
        return response("recipe_item not found", 404)
    return db_recipe_item

@router.post("/", response_model=RecipeItemOut)
async def create_recipe_item(recipe_item: RecipeItemCreate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_recipe_item = crud_recipe_item.create_recipe_item(db, recipe_item)
    return db_recipe_item

@router.put("/{recipe_item_id}/", response_model=RecipeItemOut)
async def update_recipe_item(recipe_item_id: UUID, recipe_item_update: RecipeItemUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_recipe_item = crud_recipe_item.get_recipe_item(db, recipe_item_id)
    if not db_recipe_item:
        return response("recipe_item not found", 404)
    db_recipe_item = crud_recipe_item.update_recipe_item(db, db_recipe_item, recipe_item_update)
    return db_recipe_item
