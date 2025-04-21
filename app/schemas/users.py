from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserOut(UserBase):
    id: int
