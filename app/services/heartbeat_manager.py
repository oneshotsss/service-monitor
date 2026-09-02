from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.models.heartbeat import Heartbeat
from app.models.service import Service
from app.schemas.heartbeat import HeartbeatIn
from app.services.event_manager import record_service_event


def record_heartbeat(db: Session, payload: HeartbeatIn) -> Heartbeat:
    ts = payload.timestamp or datetime.now(timezone.utc)

    # ensure service exists before inserting heartbeat (to satisfy FK)
    svc = db.get(Service, payload.service_id)
    created = False
    if svc is None:
        svc = Service(service_id=payload.service_id, name=None, status="online", last_heartbeat_at=ts)
        db.add(svc)
        # flush so service row exists for FK
        db.flush()
        created = True
        try:
            record_service_event(db, svc.service_id, None, "online", note="Service created by heartbeat")
        except Exception:
            pass
    else:
        old_status = svc.status
        svc.last_heartbeat_at = ts
        svc.status = "online"
        db.add(svc)

    # now persist heartbeat
    hb = Heartbeat(service_id=payload.service_id, timestamp=ts, latency_ms=payload.latency_ms)
    db.add(hb)

    db.commit()

    # if status changed, record event (after commit to avoid transaction issues)
    if not created and 'old_status' in locals() and old_status != "online":
        try:
            record_service_event(db, svc.service_id, old_status, "online", note="Heartbeat detected service online")
        except Exception:
            pass

    db.refresh(hb)
    return hb
