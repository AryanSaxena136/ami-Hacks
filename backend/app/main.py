from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import CORS_ORIGINS
from app.core.database import init_db
from app.routes.alerts import router as alerts_router
from app.routes.dashboard import router as dashboard_router
from app.routes.feeds import router as feeds_router
from app.routes.health import router as health_router

app = FastAPI(
    title="CityPulse API",
    description="Live civic health dashboard for weather, traffic, and incident data.",
    version="0.1.0",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": "An internal server error occurred."})

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(feeds_router)
app.include_router(alerts_router)
app.include_router(dashboard_router)


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/", summary="Root endpoint")
def read_root() -> dict[str, str]:
    return {"message": "CityPulse backend is running."}
