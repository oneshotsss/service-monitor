from datetime import datetime
from pydantic import BaseModel, Field


class HeartbeatIn(BaseModel):
    service_id: str = Field(..., max_length=100)
    timestamp: datetime | None = None
    latency_ms: int | None = None


class HeartbeatRead(BaseModel):
    id: int
    service_id: str
    timestamp: datetime
    latency_ms: int | None
    created_at: datetime

    class Config:
        orm_mode = True
