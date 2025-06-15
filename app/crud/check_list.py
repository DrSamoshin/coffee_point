import logging
from uuid import UUID
from sqlalchemy.orm import Session

from app.core.consts import CHECK_LIST_DIVIDER
from app.db.models import CheckList
from app.core.consts import CheckListTimePoint
from app.db.session import db_safe
from app.schemas.check_list import CheckListUpdate


@db_safe
def get_check_list(db: Session, time_point: CheckListTimePoint):
    logging.info(f"call method get_check_list")
    try:
        db_check_list = db.query(CheckList).filter(CheckList.time_point == time_point).first()
        if not db_check_list:
            db_check_list = CheckList(time_point=time_point,
                                      check_list="fill check list")
            db.add(db_check_list)
            db.commit()
            db.refresh(db_check_list)
        db_check_list.check_list = db_check_list.check_list.split(CHECK_LIST_DIVIDER)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"check list: {db_check_list}")
        return db_check_list

@db_safe
def update_check_list(db: Session, check_list_id: UUID, updates: CheckListUpdate):
    logging.info(f"call method update_check_list")
    try:
        db_check_list = db.query(CheckList).filter(CheckList.id == check_list_id).first()
        check_list_str = CHECK_LIST_DIVIDER.join(updates.check_list)
        db_check_list.check_list = check_list_str
        db.commit()
        db.refresh(db_check_list)
        db_check_list.check_list = db_check_list.check_list.split(CHECK_LIST_DIVIDER)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"check list is updated: {db_check_list}")
        return db_check_list
