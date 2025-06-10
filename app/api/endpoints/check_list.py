from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from uuid import UUID

from app.core.consts import CheckListTimePoint
from app.db.session import get_db
from app.crud import check_list as crud_check_list
from app.services.authentication import get_user_id_from_token
from app.schemas.check_list import CheckListOut, CheckListUpdate


router = APIRouter(prefix='/check-lists', tags=['check_lists'])

@router.get("/start/", response_model=CheckListOut)
async def get_start_check_list(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    check_list = crud_check_list.get_check_list(db, time_point=CheckListTimePoint.start_shift)
    check_list.check_list = check_list.check_list.split(",")
    return check_list

@router.get("/end/", response_model=CheckListOut)
async def get_end_check_list(db: Session = Depends(get_db), user_id: str = Depends(get_user_id_from_token)):
    check_list = crud_check_list.get_check_list(db, time_point=CheckListTimePoint.end_shift)
    check_list.check_list = check_list.check_list.split(",")
    return check_list

@router.put("/{check_list_id}/", response_model=CheckListOut)
async def update_start_check_list(check_list_id: UUID,
                                  check_list_update: CheckListUpdate,
                                  db: Session = Depends(get_db),
                                  user_id: str = Depends(get_user_id_from_token)):
    check_list = crud_check_list.update_check_list(db, check_list_id, check_list_update)
    check_list.check_list = check_list.check_list.split(",")
    return check_list
