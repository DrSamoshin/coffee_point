from fastapi import APIRouter

router = APIRouter(prefix='/cafe-data', tags=['cafe_data'])

@router.get("/")
async def get_cafe_data():
    result = {
        "name": "Coffee point",
        "address": {
            "street": "ул. Ирининская",
            "house": "25",
            "apartment": "16",
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
    return result
