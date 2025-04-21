from uuid import UUID
from pydantic import BaseModel
from decimal import Decimal


class RecipeItemBase(BaseModel):
    product_id: UUID
    item_id: UUID
    amount: Decimal

class RecipeItemCreate(RecipeItemBase):
    pass

class RecipeItemUpdate(RecipeItemBase):
    pass

class RecipeItemOut(RecipeItemBase):
    id: UUID

    model_config = {"from_attributes": True}

