import os
import time
import logging
from datetime import datetime, timezone

import httpx

SERVICE_ID = os.getenv("SERVICE_ID", "service-a")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
INTERVAL = int(os.getenv("INTERVAL", "5"))

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

client = httpx.Client(timeout=10.0)


def register_service():
    payload = {"service_id": SERVICE_ID, "name": SERVICE_ID}
    try:
        r = client.post(f"{BACKEND_URL}/services", json=payload)
        if r.status_code in (200, 201):
            logging.info("Registered service: %s", r.json())
        else:
            logging.warning("Register failed: %s %s", r.status_code, r.text)
    except Exception as e:
        logging.debug("Register error: %s", e)


def send_heartbeat():
    payload = {"service_id": SERVICE_ID, "timestamp": datetime.now(timezone.utc).isoformat(), "latency_ms": 10}
    try:
        r = client.post(f"{BACKEND_URL}/heartbeat", json=payload)
        if r.status_code in (200, 201):
            logging.info("Heartbeat sent: %s", r.json())
        else:
            logging.warning("Heartbeat failed: %s %s", r.status_code, r.text)
    except Exception:
        logging.exception("Error sending heartbeat")


if __name__ == '__main__':
    logging.info("Client starting. SERVICE_ID=%s BACKEND=%s INTERVAL=%s", SERVICE_ID, BACKEND_URL, INTERVAL)
    # try to register once
    register_service()
    while True:
        send_heartbeat()
        time.sleep(INTERVAL)
