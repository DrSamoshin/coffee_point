from fastapi import APIRouter
from app.crud import coffee_shop as crud_coffee_shop

router = APIRouter(prefix='/coffee-shop', tags=['coffee_shop'])

@router.get("/info/")
async def get_coffee_shop_info():
    return crud_coffee_shop.get_coffee_shop_info()
