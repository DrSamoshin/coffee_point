from fastapi import APIRouter
from app.core.responses import response
from app.middleware.authentication import AuthenticationMiddleware
from fastapi import Request

router = APIRouter(prefix='/health', tags=['health'])

@router.get("/app")
async def get_health_check():
    return response("application is running", 200, "success")

@router.get("/token")
async def check_token(request: Request):
    await AuthenticationMiddleware.check_token(request)
    return response("token is valid", 200, "success")