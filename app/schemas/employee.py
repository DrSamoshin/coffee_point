from uuid import UUID
from pydantic import BaseModel
from app.core.consts import EmployeePosition


class EmployeeBase(BaseModel):
    name: str
    position: EmployeePosition

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeOut(EmployeeBase):
    id: UUID
    active: bool

    model_config = {"from_attributes": True}

class BaristaOut(BaseModel):
    id: UUID
    name: str

    model_config = {"from_attributes": True}
