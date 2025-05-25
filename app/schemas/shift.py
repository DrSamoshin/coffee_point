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

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            active=obj.active,
            employee_id=obj.employee_id,
            start_time=obj.start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            end_time=obj.end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        )

    model_config = {"from_attributes": True}