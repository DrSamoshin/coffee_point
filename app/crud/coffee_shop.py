import logging
from app.core.consts import coffee_shop_info


def get_coffee_shop_info():
    logging.info("call method get_coffee_shop_info")
    return coffee_shop_info
