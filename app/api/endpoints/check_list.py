from fastapi import APIRouter, Depends
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/check-list', tags=['check_list'])

@router.get("/")
async def get_check_list(user_id: str = Depends(get_user_id_from_token)):
    result = ["fresh_water", "cleaned_table"]
    return result
