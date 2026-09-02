from typing import Optional

from sqlalchemy.orm import Session

from app.models.service_event import ServiceEvent


def record_service_event(db: Session, service_id: str, old_status: Optional[str], new_status: str, note: Optional[str] = None) -> ServiceEvent:
    ev = ServiceEvent(service_id=service_id, old_status=old_status, new_status=new_status, note=note)
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev
