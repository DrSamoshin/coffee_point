import os
import logging
from pathlib import Path
from fastapi import FastAPI
from app.core.configs import settings
from app.api.endpoints import (cafe_data_router,
                               category_router,
                               check_list_router,
                               client_router,
                               employee_router,
                               health_router,
                               item_router,
                               order_router,
                               product_router,
                               product_order_router,
                               product_tag_router,
                               recipe_item_router,
                               shift_router,
                               store_item_router,
                               supplier_router,
                               supply_router,
                               tag_router,
                               user_router)

BASE_DIR = Path(__file__).resolve().parent
contents = os.listdir(BASE_DIR)
main_app = FastAPI()

# routers
main_app.include_router(cafe_data_router)
main_app.include_router(category_router)
main_app.include_router(check_list_router)
main_app.include_router(client_router)
main_app.include_router(employee_router)
main_app.include_router(health_router)
main_app.include_router(item_router)
main_app.include_router(order_router)
main_app.include_router(product_router)
main_app.include_router(product_order_router)
main_app.include_router(product_tag_router)
main_app.include_router(recipe_item_router)
main_app.include_router(shift_router)
main_app.include_router(store_item_router)
main_app.include_router(supplier_router)
main_app.include_router(supply_router)
main_app.include_router(tag_router)
main_app.include_router(user_router)

logging.info("Starting FastAPI")
logging.info(f"DB url: %s", settings.data_base.sqlalchemy_url)
logging.info(f"Folder contents %s: %s", BASE_DIR, contents)


