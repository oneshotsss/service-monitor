from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.database.session import init_db
from app.services.status_checker import start_status_checker


app = FastAPI(title="Service Monitor")
# mount static files (CSS/JS) — use relative path so it works inside container
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(api_router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    # start background thread to mark services offline when heartbeats stop
    start_status_checker()
