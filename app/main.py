from pathlib import Path

from fastapi import FastAPI

from app.api.endpoints.health_checks import router as health_router

BASE_DIR = Path(__file__).resolve().parent
main_app = FastAPI()

# routers
main_app.include_router(health_router, tags=["health"])