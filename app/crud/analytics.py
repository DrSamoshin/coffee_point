import logging
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.db.models import Order
from app.db.db_sessions import db_safe
from app.core.consts import OrderStatus


def _get_total_sales(db: Session, shift_id: UUID):
    total_sales = db.query(func.sum(Order.price)) \
        .filter(Order.shift_id == shift_id, Order.debit == False) \
        .scalar()
    return total_sales

def _get_total_returns(db: Session, shift_id: UUID):
    total_returns = db.query(func.sum(Order.price)) \
        .filter(Order.shift_id == shift_id, Order.debit) \
        .scalar()
    return total_returns

@db_safe
def get_shift_income(db: Session, shift_id: UUID):
    logging.info(f"call method get_shift_income")
    try:
        total_sales = _get_total_sales(db, shift_id)
        total_returns = _get_total_returns(db, shift_id)
        net_total = (total_sales or 0) - (total_returns or 0)
    except Exception as error:
            logging.error(error)
    else:
        logging.info(f"shift income: {net_total}")
        return {"income": net_total}
