from uuid import UUID
from pydantic import BaseModel

class ProductTagBase(BaseModel):
    name: str
    product_id: UUID
    tag_id: UUID

class ProductTagCreate(ProductTagBase):
    pass

class ProductTagUpdate(ProductTagBase):
    pass

class ProductTagOut(ProductTagBase):
    id: UUID

    model_config = {"from_attributes": True}

