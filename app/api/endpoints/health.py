from fastapi import APIRouter, Depends
from app.core.responses import response
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix='/health', tags=['health'])

@router.get("/app/")
async def get_health_check():
    return response("application is running", 200, "success")

@router.get("/token/")
async def check_token(user_id: str = Depends(get_user_id_from_token)):
    return response("token is valid", 200, "success")