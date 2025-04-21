from uuid import UUID

from pydantic import BaseModel, ConfigDict
from typing import Optional

class EmployeeBase(BaseModel):
    name: Optional[str] = None

    def __str__(self):
        return f"name: {self.name}"

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeOut(EmployeeBase):

    id: UUID
    active: bool

    def __str__(self):
        return (f"id: {self.id}\n"
                f"name: {self.name}\n"
                f"active: {self.active}\n")
