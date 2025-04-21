from pathlib import Path

from fastapi import FastAPI

from app.api.endpoints import health_router, user_router, employee_router, shift_router


BASE_DIR = Path(__file__).resolve().parent
main_app = FastAPI()

# routers
main_app.include_router(health_router, prefix="/health", tags=["health"])
main_app.include_router(user_router, prefix="/users", tags=["users"])
main_app.include_router(employee_router, prefix="/employees", tags=["employees"])
main_app.include_router(shift_router, prefix="/shifts", tags=["shifts"])

