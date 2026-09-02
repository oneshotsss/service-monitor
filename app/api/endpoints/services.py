from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.service import ServiceRegister, ServiceRead
from app.services.service_manager import create_or_update_service, get_service, list_services

router = APIRouter(prefix="/services", tags=["services"])


@router.post("", response_model=ServiceRead, status_code=status.HTTP_201_CREATED)
def register_service(payload: ServiceRegister, db: Session = Depends(get_db)):
    svc = create_or_update_service(db, payload)
    return svc


@router.get("", response_model=list[ServiceRead])
def read_services(db: Session = Depends(get_db)):
    return list_services(db)


@router.get("/{service_id}", response_model=ServiceRead)
def read_service(service_id: str, db: Session = Depends(get_db)):
    svc = get_service(db, service_id)
    if svc is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return svc
