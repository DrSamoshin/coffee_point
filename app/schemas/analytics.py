from decimal import Decimal
from pydantic import BaseModel


class ShiftIncomeOut(BaseModel):
    income: Decimal

    model_config = {"from_attributes": True}
