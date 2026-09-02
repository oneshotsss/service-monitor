from collections.abc import Generator
import time

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import DATABASE_URL
from app.database.base import Base


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(retries: int = 10, delay: float = 1.0) -> None:
    """Initialize database schema, retrying connection if DB is not ready yet."""
    from app import models  # noqa: F401

    last_err = None
    for i in range(retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            # connected
            last_err = None
            break
        except Exception as exc:  # pragma: no cover - retry logic
            last_err = exc
            time.sleep(delay)
    if last_err is not None:
        # final attempt will raise the original exception
        with engine.connect() as conn:  # if this fails it will raise
            conn.execute(text("SELECT 1"))

    Base.metadata.create_all(bind=engine)
