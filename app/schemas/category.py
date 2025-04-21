from pydantic import BaseModel
from uuid import UUID

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: UUID

    model_config = {"from_attributes": True}