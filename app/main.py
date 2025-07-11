import os
import logging
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.core.configs import settings
from app.api.endpoints import (admin_router,
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
                               user_router)

BASE_DIR = Path(__file__).resolve().parent
contents = os.listdir(BASE_DIR)
main_app = FastAPI(
    openapi_version=settings.app_data.openapi_version,
)

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://coffee-point-crm.web.app",
        "http://localhost:5173"   # для Vite dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if main_app.openapi_schema:
        return main_app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.app_data.title,
        version=settings.app_data.version,
        description=settings.app_data.description,
        routes=main_app.routes,
    )

    def transform_anyof(schema: dict):
        if not isinstance(schema, dict):
            return

        keys = list(schema.keys())
        for key in keys:
            value = schema.get(key)
            if isinstance(value, dict):
                transform_anyof(value)
            elif key == "anyOf":
                types = [t.get("type") for t in value if isinstance(t, dict) and "type" in t]
                if "null" in types:
                    actual_types = [t for t in types if t != "null"]
                    if len(actual_types) == 1:
                        schema.pop("anyOf")
                        schema["type"] = [actual_types[0], "null"]

    for schema in openapi_schema.get("components", {}).get("schemas", {}).values():
        transform_anyof(schema)

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
logging.info(f"DB url: %s", settings.data_base.get_db_url('users'))


