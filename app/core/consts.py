from enum import Enum

class PaymentMethod(str, Enum):
    cash = "cash"
    card = "card"

class Type(str, Enum):
    dine_in = "dine_in"
    delivery = "delivery"
    takeout = "takeout"