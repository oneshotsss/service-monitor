from datetime import datetime, timezone
from typing import Iterable, Optional

from sqlalchemy.orm import Session

from app.models.service import Service
from app.schemas.service import ServiceRegister


def create_or_update_service(db: Session, payload: ServiceRegister) -> Service:
    svc = db.get(Service, payload.service_id)
    now = datetime.now(timezone.utc)
    if svc is None:
        svc = Service(
            service_id=payload.service_id,
            name=payload.name,
            status="online",
            last_heartbeat_at=now,
        )
        db.add(svc)
    else:
        svc.name = payload.name
        svc.status = "online"
        svc.last_heartbeat_at = now
    db.commit()
    db.refresh(svc)
    return svc


def get_service(db: Session, service_id: str) -> Optional[Service]:
    return db.get(Service, service_id)


def list_services(db: Session) -> Iterable[Service]:
    return db.query(Service).order_by(Service.service_id).all()
