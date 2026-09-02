import threading
import time
from datetime import datetime, timezone

from app.database.session import SessionLocal
from app.core.config import HEARTBEAT_TIMEOUT_SECONDS, STATUS_CHECK_INTERVAL_SECONDS
from app.models.service import Service
from app.services.event_manager import record_service_event


def _checker_loop() -> None:
    while True:
        db = SessionLocal()
        try:
            now = datetime.now(timezone.utc)
            services = db.query(Service).all()
            for svc in services:
                last = svc.last_heartbeat_at
                if last is None:
                    continue
                delta = (now - last).total_seconds()
                if delta > HEARTBEAT_TIMEOUT_SECONDS:
                    if svc.status != "offline":
                        old = svc.status
                        svc.status = "offline"
                        db.add(svc)
                        db.commit()
                        try:
                            record_service_event(db, svc.service_id, old, "offline", note=f"No heartbeat for {int(delta)}s")
                        except Exception:
                            # don't let event logging break the loop
                            pass
        finally:
            db.close()
        time.sleep(STATUS_CHECK_INTERVAL_SECONDS)


def start_status_checker() -> None:
    t = threading.Thread(target=_checker_loop, daemon=True)
    t.start()
