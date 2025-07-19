import os
import logging
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.core.configs import settings
from app.api.endpoints import (
    admin_router,
    analytics_router,
    category_router,
    check_list_router,
    client_router,
    coffee_shop_router,
    constants_router,
    employee_router,
    employee_shift_router,
    files_router,
    health_router,
    item_router,
    order_router,
    orders_report_router,
    product_router,
    product_order_router,
    recipe_item_router,
    shift_router,
    store_item_router,
    supplier_router,
    supply_router,
    user_router,
)

BASE_DIR = Path(__file__).resolve().parent
contents = os.listdir(BASE_DIR)
main_app = FastAPI(
    openapi_version=settings.app_data.openapi_version,
)

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://coffee-point-crm.web.app",
        "http://localhost:5173",  # для Vite dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    if main_app.openapi_schema:
        return main_app.openapi_schema

    def fix_nullable(schema: dict):
        if isinstance(schema, dict):
            keys = list(schema.keys())
            if "anyOf" in keys and len(schema["anyOf"]) == 2:
                types = set(item.get("type") for item in schema["anyOf"])
                if "null" in types:
                    non_null = next(
                        item for item in schema["anyOf"] if item.get("type") != "null"
                    )
                    nullable_type = [non_null["type"], "null"]
                    schema.pop("anyOf")
                    schema["type"] = nullable_type
                    if "format" in non_null:
                        schema["format"] = non_null["format"]
            else:
                for v in schema.values():
                    fix_nullable(v)
        elif isinstance(schema, list):
            for item in schema:
                fix_nullable(item)

    openapi_schema = get_openapi(
        title=settings.app_data.title,
        version=settings.app_data.version,
        description=settings.app_data.description,
        routes=main_app.routes,
        openapi_version="3.1.0",
    )

    openapi_schema["servers"] = [
        {
            "url": "https://coffee-point-api-317780828805.europe-west3.run.app",
            "description": "Production",
        },
        {"url": "http://127.0.0.1:8080", "description": "Local"},
    ]

    fix_nullable(openapi_schema)

    main_app.openapi_schema = openapi_schema
    return main_app.openapi_schema


main_app.openapi = custom_openapi

# routers
main_app.include_router(analytics_router)
main_app.include_router(category_router)
main_app.include_router(check_list_router)
main_app.include_router(client_router)
main_app.include_router(coffee_shop_router)
main_app.include_router(constants_router)
main_app.include_router(employee_router)
main_app.include_router(employee_shift_router)
main_app.include_router(files_router)
main_app.include_router(health_router)
main_app.include_router(item_router)
main_app.include_router(order_router)
main_app.include_router(orders_report_router)
main_app.include_router(product_router)
main_app.include_router(product_order_router)
main_app.include_router(recipe_item_router)
main_app.include_router(shift_router)
main_app.include_router(store_item_router)
main_app.include_router(supplier_router)
main_app.include_router(supply_router)

if settings.run.ADMIN_MODE:
    main_app.include_router(admin_router)
    main_app.include_router(user_router)

logging.info("admin mode: %s", settings.run.ADMIN_MODE)
logging.info("starting FastAPI")
logging.info("DB url: %s", settings.data_base.get_db_url("users"))
