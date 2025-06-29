import logging
from datetime import datetime, timezone
from sqlalchemy import desc

from sqlalchemy.orm import Session
from app.db.models import ReportingPeriod
from app.db.session import db_safe


@db_safe
def get_reporting_periods(db: Session):
    logging.info(f"call method get_reporting_periods")
    try:
        db_reporting_periods = db.query(ReportingPeriod).filter().order_by(desc(ReportingPeriod.start_time)).all()
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"reporting periods: {len(db_reporting_periods)}")
        return db_reporting_periods


@db_safe
def create_reporting_period(db: Session):
    logging.info(f"call method create_reporting_period")
    try:
        with db.begin():
            if db_last_reporting_period:= db.query(ReportingPeriod).order_by(desc(ReportingPeriod.start_time)).first():
                db_last_reporting_period.end_time = datetime.now(timezone.utc)
                db_last_reporting_period.active = False
            db_new_reporting_period = ReportingPeriod(start_time=datetime.now(timezone.utc))
            db.add(db_new_reporting_period)
            db.flush()
            db.refresh(db_new_reporting_period)
    except Exception as error:
        logging.error(error)
    else:
        logging.info(f"reporting_period is created: {db_new_reporting_period}")
        return db_new_reporting_period
