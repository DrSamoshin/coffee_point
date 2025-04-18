from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def get_health_check() -> dict:
    msg = "application is running"
    return {"message": msg}