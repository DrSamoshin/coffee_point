from fastapi import APIRouter
from app.core.consts import EmployeePosition, ItemMeasurements, OrderPaymentMethod, OrderType, OrderStatus

router = APIRouter(prefix='/constants', tags=['constants'])


def enum_to_list(enum_cls):
    return [{"key": e.name, "value": e.value} for e in enum_cls]

@router.get("/payment-methods/")
def get_payment_methods():
    return enum_to_list(OrderPaymentMethod)

@router.get("/order-types/")
def get_order_types():
    return enum_to_list(OrderType)

@router.get("/order-statuses/")
def get_order_statuses():
    return enum_to_list(OrderStatus)

@router.get("/employee-positions/")
def get_employee_positions():
    return enum_to_list(EmployeePosition)

@router.get("/item-measurements/")
def get_item_measurements():
    return enum_to_list(ItemMeasurements)

