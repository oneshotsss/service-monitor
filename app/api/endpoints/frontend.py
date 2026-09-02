from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@router.get("/services/{service_id}/open", response_class=HTMLResponse)
def service_detail(request: Request, service_id: str):
    return templates.TemplateResponse(request=request, name="service.html", context={"service_id": service_id})
