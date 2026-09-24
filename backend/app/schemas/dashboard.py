from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ZoneHealth(BaseModel):
    zone: str
    score: int
    status: str
    latitude: float | None = None
    longitude: float | None = None


class ZoneSignal(BaseModel):
    source: str
    data_type: str
    value: float
    unit: str | None = None
    severity: str | None = None
    zone: str
    latitude: float | None = None
    longitude: float | None = None
    timestamp: datetime


class DashboardResponse(BaseModel):
    city_score: int
    status: str
    zones: list[ZoneHealth]
    latest_signals: list[ZoneSignal]
    active_alerts: list[dict]
    summary: str
    last_updated: datetime
