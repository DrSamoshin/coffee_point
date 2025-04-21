from fastapi import APIRouter

from app.core.responses import response

router = APIRouter()

@router.get("/health")
def get_health_check():
    return response("application is running", 200, "success")