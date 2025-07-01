from enum import Enum

CHECK_LIST_DIVIDER = "#"

class OrderPaymentMethod(str, Enum):
    cash = "cash"
    card = "card"

class OrderType(str, Enum):
    dine_in = "dine_in"
    delivery = "delivery"
    takeaway = "takeaway"

class OrderStatus(str, Enum):
    waiting = "waiting"
    completed = "completed"
    cancelled = "cancelled"

class EmployeePosition(str, Enum):
    barista = "barista"
    manager = "manager"

class ItemMeasurements(str, Enum):
    kilogram = "kg"
    gram = "g"
    liter = "l"
    milliliter = "ml"
    piece = "pcs"

class CheckListTimePoint(str, Enum):
    start_shift = "start_shift"
    end_shift = "end_shift"

coffee_shop_info = {
    "name": "Coffee point",
    "address": {
        "street": "ул. Ирининская",
        "house": "25",
        "apartment": "17",
        "city": "Гомель",
        "postcode": "246050",
        "country": "Беларусь"
    },
    "contacts": {
        "phone": "+375 (29) 358-42-05",
        "email": "info@coffee-point.by",
        "website": "https://coffee-point.by"
    },
    "opening_hours": {
        "mon-fri": "08:00–21:00",
        "sat-sun": "08:00–21:00"
    },
    "location": {
        "latitude": 52.427994805668774,
        "longitude": 31.002229061074484,
        "map_link": "https://maps.app.goo.gl/Y16CRftu8jigYthW7"
    }
}