from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class UserBase(BaseModel):
    name: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserOut(UserBase):
    id: UUID
    deactivated: bool

    model_config = {"from_attributes": True}
