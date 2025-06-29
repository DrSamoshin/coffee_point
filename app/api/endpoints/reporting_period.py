from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.reporting_period import ReportingPeriodOut
from app.crud import reporting_period as crud_reporting_period
from app.services.authentication import get_user_id_from_token


router = APIRouter(prefix='/reporting-periods', tags=['reporting_periods'])

@router.get("/reporting-periods/", response_model=list[ReportingPeriodOut])
async def get_reporting_periods(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_reporting_periods = crud_reporting_period.get_reporting_periods(db)
    return db_reporting_periods

@router.post("/", response_model=ReportingPeriodOut)
async def create_reporting_period(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    db_reporting_period = crud_reporting_period.create_reporting_period(db)
    return db_reporting_period




