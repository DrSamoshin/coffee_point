from uuid import UUID

from pydantic import BaseModel
from typing import Optional

class EmployeeBase(BaseModel):
    name: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeOut(EmployeeBase):
    id: UUID
    active: bool

    model_config = {"from_attributes": True}

