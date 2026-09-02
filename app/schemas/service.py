from datetime import datetime
from pydantic import BaseModel, Field


class ServiceRegister(BaseModel):
    service_id: str = Field(..., max_length=100)
    name: str | None = Field(None, max_length=255)


class ServiceRead(BaseModel):
    service_id: str
    name: str | None
    status: str
    last_heartbeat_at: datetime | None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
