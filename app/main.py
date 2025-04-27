from pathlib import Path

from fastapi import FastAPI
from app.middleware.authentication import AuthenticationMiddleware

from app.api.endpoints import (category_router,
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
main_app = FastAPI()

main_app.add_middleware(AuthenticationMiddleware)

# routers
main_app.include_router(category_router, prefix="/category", tags=["category"])
main_app.include_router(client_router, prefix="/client", tags=["client"])
main_app.include_router(employee_router, prefix="/employee", tags=["employee"])
main_app.include_router(health_router, tags=["health"])
main_app.include_router(item_router, prefix="/item", tags=["item"])
main_app.include_router(order_router, prefix="/order", tags=["order"])
main_app.include_router(product_router, prefix="/product", tags=["product"])
main_app.include_router(product_order_router, prefix="/product_order", tags=["product_order"])
main_app.include_router(product_tag_router, prefix="/product_tag", tags=["product_tag"])
main_app.include_router(recipe_item_router, prefix="/recipe_item", tags=["recipe_item"])
main_app.include_router(shift_router, prefix="/shift", tags=["shift"])
main_app.include_router(store_item_router, prefix="/store_item", tags=["store_item"])
main_app.include_router(supplier_router, prefix="/supplier", tags=["supplier"])
main_app.include_router(supply_router, prefix="/supply", tags=["supply"])
main_app.include_router(tag_router, prefix="/tag", tags=["tag"])
main_app.include_router(user_router, prefix="/user", tags=["user"])


