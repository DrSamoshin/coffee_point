from enum import Enum

class OrderPaymentMethod(str, Enum):
    cash = "cash"
    card = "card"

class OrderType(str, Enum):
    dine_in = "dine_in"
    delivery = "delivery"
    takeout = "takeout"

class OrderStatus(str, Enum):
    waiting = "waiting"
    completed = "completed"
    cancelled = "cancelled"
    returned = "returned"

class EmployeePosition(str, Enum):
    barista = "barista"
    manager = "manager"