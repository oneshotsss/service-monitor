from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.heartbeat import HeartbeatRead
from app.schemas.service import ServiceRead
from app.schemas.heartbeat import HeartbeatIn
from app.services.metrics_manager import latency_stats, outage_count, uptime_downtime
from app.models.heartbeat import Heartbeat
from app.models.service_event import ServiceEvent

router = APIRouter(prefix="/services/{service_id}", tags=["services-detail"])


@router.get("", response_model=ServiceRead)
def get_service_detail(service_id: str, db: Session = Depends(get_db)):
    svc = db.get(__import__("app.models").models.Service, service_id)
    if svc is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Service not found")
    return svc


@router.get("/heartbeats", response_model=list[HeartbeatRead])
def list_heartbeats(service_id: str, limit: int = Query(50, ge=1, le=1000), db: Session = Depends(get_db)):
    q = db.query(Heartbeat).filter(Heartbeat.service_id == service_id).order_by(Heartbeat.timestamp.desc()).limit(limit)
    return q.all()


@router.get("/events")
def list_events(service_id: str, limit: int = Query(50, ge=1, le=1000), db: Session = Depends(get_db)):
    q = db.query(ServiceEvent).filter(ServiceEvent.service_id == service_id).order_by(ServiceEvent.timestamp.desc()).limit(limit)
    return [
        {"id": e.id, "service_id": e.service_id, "old_status": e.old_status, "new_status": e.new_status, "timestamp": e.timestamp.isoformat(), "note": e.note}
        for e in q.all()
    ]


@router.get("/metrics")
def get_metrics(service_id: str, db: Session = Depends(get_db)):
    lat = latency_stats(db, service_id)
    outages = outage_count(db, service_id)
    updown = uptime_downtime(db, service_id)
    return {**lat, "outages": outages, **updown}
