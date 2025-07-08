import logging
from fastapi import HTTPException
from uuid import UUID
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from app.db.models import Order, Shift
from app.crud import order as crud_order


def get_shift_report(db: Session, shift_id: UUID):
    logging.info(f"call method get_shift_orders")
    result = dict()
    try:
        db_shift_orders = crud_order.get_shift_orders(shift_id, db)
    except Exception as error:
        logging.error(error)
        raise HTTPException(status_code=500, detail="unexpected error during shift orders fetch")
    else:

        shift_income = 0
        order_amount = 0
        total_product_amount = 0
        products_amount = dict()
        product_price = dict()
        for order in db_shift_orders:

            if order.debit:
                shift_income = shift_income - float(order.price)
                order_amount = order_amount - 1
                total_product_amount = total_product_amount - len(order.products)
                for product in order.products:
                    product_name = product.product_name
                    if products_amount.get(product_name) is None:
                        products_amount[product_name] = float(product.count)
                    else:
                        products_amount[product_name] = products_amount[product_name] - float(product.count)
                    if product_price.get(product_name) is None:
                        product_price[product_name] = float(product.product_price)
                    else:
                        product_price[product_name] = product_price[product_name] - float(product.product_price)
            else:

                shift_income = shift_income + float(order.price)

                order_amount = order_amount + 1
                total_product_amount = total_product_amount + len(order.products)
                for product in order.products:
                    product_name = product.product_name
                    if products_amount.get(product_name) is None:
                        products_amount[product_name] = float(product.count)
                    else:
                        products_amount[product_name] = products_amount[product_name] + float(product.count)
                    if product_price.get(product_name) is None:
                        product_price[product_name] = float(product.product_price)
                    else:
                        product_price[product_name] = product_price[product_name] + float(product.product_price)


        result['shift_income'] = shift_income
        result['order_amount'] = order_amount
        result['total_product_amount'] = total_product_amount
        result['products_amount'] = dict(sorted(products_amount.items(), key=lambda item: item[1], reverse=True))
        result['product_price'] = dict(sorted(product_price.items(), key=lambda item: item[1], reverse=True))

        logging.info(f"result: {result}")
        return result


def get_active_shift_report(db: Session):
    logging.info(f"call method get_active_shift_income")
    try:
        db_shift = db.query(Shift).filter(Shift.active == True).first()
        active_shift_report = get_shift_report(db, db_shift.id)
    except Exception as error:
        logging.error(error)
        raise HTTPException(status_code=500, detail="unexpected error during shift orders fetch")
    else:
        logging.info(f"active shift report: {active_shift_report}")
        return active_shift_report