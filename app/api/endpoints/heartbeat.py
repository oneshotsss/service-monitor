from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.heartbeat import HeartbeatIn, HeartbeatRead
from app.services.heartbeat_manager import record_heartbeat

router = APIRouter()


@router.post("/heartbeat", response_model=HeartbeatRead, status_code=status.HTTP_201_CREATED)
def post_heartbeat(payload: HeartbeatIn, db: Session = Depends(get_db)):
    hb = record_heartbeat(db, payload)
    return hb
