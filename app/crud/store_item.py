import logging
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from decimal import Decimal

from app.db.models import StoreItem, ReportingPeriod, Supply, Supplier
from app.db.session import db_safe
from app.schemas.store_item import StoreItemCreate, StoreItemUpdate, StoreItemOut, CalculationStoreItemOut


@db_safe
def get_store_item(db: Session, store_item_id: UUID):
    logging.info(f"call method get_store_item")
    try:
        db_store_item = db.query(StoreItem).filter(StoreItem.id == store_item_id).options(
            joinedload(StoreItem.supply).joinedload(Supply.supplier)).first()
        supplier = None
        if db_store_item.supply and db_store_item.supply.supplier:
            supplier = db_store_item.supply.supplier.name
        store_item = StoreItemOut(id=db_store_item.id,
                                  item_id=db_store_item.item_id,
                                  item_name=db_store_item.item.name,
                                  amount=db_store_item.amount,
                                  price_per_item=db_store_item.price_per_item,
                                  reporting_period_id=db_store_item.reporting_period_id,
                                  date=db_store_item.date,
                                  debit=db_store_item.debit,
                                  supply_id=db_store_item.supply_id,
                                  supplier=supplier)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"store_item: {store_item}")
        return store_item

@db_safe
def get_store_items(db: Session):
    logging.info(f"call method get_store_items")
    try:
        db_reporting_period = db.query(ReportingPeriod).filter(ReportingPeriod.active == True).first()
        store_items = []
        db_store_items = db.query(StoreItem).filter(StoreItem.reporting_period_id == db_reporting_period.id).order_by(desc(StoreItem.date)).all()
        for db_store_item in db_store_items:
            supplier = None
            if db_store_item.supply and db_store_item.supply.supplier:
                supplier = db_store_item.supply.supplier.name
            store_item = StoreItemOut(id=db_store_item.id,
                                      item_id=db_store_item.item_id,
                                      item_name=db_store_item.item.name,
                                      amount=db_store_item.amount,
                                      price_per_item=db_store_item.price_per_item,
                                      reporting_period_id=db_store_item.reporting_period_id,
                                      date=db_store_item.date,
                                      debit=db_store_item.debit,
                                      supply_id=db_store_item.supply_id,
                                      supplier=supplier)
            store_items.append(store_item)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"store_items: {len(store_items)}")
        return store_items

@db_safe
def get_store_items_calculation(db: Session):
    store_items_calculation = {}
    store_items = get_store_items(db)

    for store_item in store_items:
        item_id = store_item.item_id
        item_name = store_item.item_name
        if not store_items_calculation.get(item_id):
            store_items_calculation[item_id] = {"amount": Decimal(0),
                                        "item_id": item_id,
                                        "item_name": item_name}

        if store_item.debit:
            store_items_calculation[item_id]["amount"] = store_items_calculation[item_id]["amount"] - Decimal(store_item.amount)
        else:
            store_items_calculation[item_id]["amount"] = store_items_calculation[item_id]["amount"] + Decimal(store_item.amount)

    store_items_calculation = [CalculationStoreItemOut(item_id=value.get("item_id"),
                                                       item_name=value.get("item_name"),
                                                       amount=value.get("amount")) for key, value in store_items_calculation.items()]
    return store_items_calculation

@db_safe
def add_store_item(db: Session, store_item: StoreItemCreate):
    logging.info(f"call method create_store_item")
    try:
        db_reporting_period = db.query(ReportingPeriod).filter(ReportingPeriod.active == True).first()
        db_store_item = StoreItem(item_id=store_item.item_id,
                                  amount=store_item.amount,
                                  price_per_item=store_item.price_per_item,
                                  date=datetime.now(timezone.utc),
                                  debit=False,
                                  supply_id=store_item.supply_id,
                                  reporting_period_id=db_reporting_period.id)
        db.add(db_store_item)
        db.commit()
        db.refresh(db_store_item)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"store_item is added: {db_store_item}")
        return db_store_item

@db_safe
def remove_store_item(db: Session, store_item: StoreItemCreate):
    logging.info(f"call method remove_store_item")
    try:
        db_reporting_period = db.query(ReportingPeriod).filter(ReportingPeriod.active == True).first()
        db_store_item = StoreItem(item_id=store_item.item_id,
                                  amount=store_item.amount,
                                  price_per_item=store_item.price_per_item,
                                  date=datetime.now(timezone.utc),
                                  debit=True,
                                  supply_id=store_item.supply_id,
                                  reporting_period_id=db_reporting_period.id)
        db.add(db_store_item)
        db.commit()
        db.refresh(db_store_item)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"store_item is removed: {db_store_item}")
        return db_store_item

@db_safe
def update_store_item(db: Session, store_item_id: UUID, updates: StoreItemUpdate):
    logging.info(f"call method update_store_item")
    print(updates)
    try:
        db_store_item = db.query(StoreItem).filter(StoreItem.id == store_item_id).first()
        for field, value in updates.model_dump().items():
            setattr(db_store_item, field, value)
        db.commit()
        db.refresh(db_store_item)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"store_item is updated: {db_store_item}")
        return db_store_item
