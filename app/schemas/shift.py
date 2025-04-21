from typing import Optional

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ShiftBase(BaseModel):
    start_time: datetime
    end_time: datetime

class ShiftCreate(ShiftBase):
    employee_id: UUID
    end_time: Optional[datetime]

class ShiftUpdate(ShiftBase):
    pass

class ShiftOut(ShiftBase):
    id: UUID
    employee_id: UUID

    model_config = {"from_attributes": True}