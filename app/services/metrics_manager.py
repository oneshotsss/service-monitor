from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.heartbeat import Heartbeat
from app.models.service import Service
from app.models.service_event import ServiceEvent


def latency_stats(db: Session, service_id: str) -> dict[str, Optional[float]]:
    avg_v, min_v, max_v = db.query(func.avg(Heartbeat.latency_ms), func.min(Heartbeat.latency_ms), func.max(Heartbeat.latency_ms)).filter(Heartbeat.service_id == service_id).one()
    return {"avg_ms": float(avg_v) if avg_v is not None else None, "min_ms": min_v, "max_ms": max_v}


def outage_count(db: Session, service_id: str) -> int:
    return db.query(func.count()).select_from(ServiceEvent).filter(ServiceEvent.service_id == service_id, ServiceEvent.new_status == "offline").scalar() or 0


def uptime_downtime(db: Session, service_id: str) -> dict[str, float]:
    svc = db.get(Service, service_id)
    if svc is None or svc.created_at is None:
        return {"uptime_seconds": 0.0, "downtime_seconds": 0.0, "total_seconds": 0.0}

    events = db.query(ServiceEvent).filter(ServiceEvent.service_id == service_id).order_by(ServiceEvent.timestamp).all()
    now = datetime.now(timezone.utc)
    # normalize created_at to aware
    created_at = svc.created_at
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    total_seconds = (now - created_at).total_seconds()

    downtime = 0.0
    i = 0
    while i < len(events):
        ev = events[i]
        if ev.new_status == "offline":
            # find next online
            j = i + 1
            while j < len(events) and events[j].new_status != "online":
                j += 1
            if j < len(events):
                end_ts = events[j].timestamp
            else:
                end_ts = now
            # normalize timestamps
            start_ts = ev.timestamp
            if start_ts.tzinfo is None:
                start_ts = start_ts.replace(tzinfo=timezone.utc)
            if end_ts.tzinfo is None:
                end_ts = end_ts.replace(tzinfo=timezone.utc)
            downtime += (end_ts - start_ts).total_seconds()
            i = j
        else:
            i += 1

    uptime = max(0.0, total_seconds - downtime)
    return {"uptime_seconds": uptime, "downtime_seconds": downtime, "total_seconds": total_seconds}
