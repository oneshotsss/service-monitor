import os


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/service_monitor",
)

HEARTBEAT_TIMEOUT_SECONDS = int(os.getenv("HEARTBEAT_TIMEOUT_SECONDS", "15"))
STATUS_CHECK_INTERVAL_SECONDS = int(os.getenv("STATUS_CHECK_INTERVAL_SECONDS", "5"))
