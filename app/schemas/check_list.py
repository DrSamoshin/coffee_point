from pydantic import BaseModel
from uuid import UUID


class CheckListBase(BaseModel):
    check_list: list[str]


class CheckListCreate(CheckListBase):
    pass


class CheckListUpdate(CheckListBase):
    pass


class CheckListOut(CheckListBase):
    id: UUID
