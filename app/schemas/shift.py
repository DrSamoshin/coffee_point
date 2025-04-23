from typing import Optional

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ShiftBase(BaseModel):
    start_time: datetime
    end_time: datetime
    employee_id: UUID

class ShiftCreate(ShiftBase):
    pass

class ShiftUpdate(ShiftBase):
    pass

class ShiftOut(ShiftBase):
    id: UUID
    active: bool

    model_config = {"from_attributes": True}