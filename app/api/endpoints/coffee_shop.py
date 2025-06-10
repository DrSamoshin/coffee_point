from fastapi import APIRouter
from app.core.consts import coffee_shop_info

router = APIRouter(prefix='/coffee-shop', tags=['coffee_shop'])

@router.get("/info/")
async def get_coffee_shop_info():
    return coffee_shop_info
