from uuid import UUID
from pydantic import BaseModel

class SupplierBase(BaseModel):
    name: str

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(SupplierBase):
    pass

class SupplierOut(SupplierBase):
    id: UUID
    deactivated: bool

    model_config = {"from_attributes": True}

