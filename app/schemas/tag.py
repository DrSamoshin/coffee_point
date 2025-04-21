from uuid import UUID
from pydantic import BaseModel


class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    pass

class TagOut(TagBase):
    id: UUID

    model_config = {"from_attributes": True}

