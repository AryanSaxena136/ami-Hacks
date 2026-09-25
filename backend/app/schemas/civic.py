from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class CivicDataCreate(BaseModel):
    source: str
    data_type: str
    value: float
    unit: str | None = None
    severity: str | None = None
    zone: str
    latitude: float | None = None
    longitude: float | None = None
    timestamp: datetime | str
    metadata: dict[str, Any] | None = None


class CivicDataPublic(BaseModel):
    id: int | None = None
    source: str
    data_type: str
    value: float
    unit: str | None = None
    severity: str | None = None
    zone: str
    latitude: float | None = None
    longitude: float | None = None
    timestamp: datetime
    metadata: dict[str, Any] | None = None


class AlertCreate(BaseModel):
    zone: str
    alert_type: str
    severity: str
    title: str
    description: str
    supporting_signals: list[str] | None = None
    timestamp: datetime | str
    metadata: dict[str, Any] | None = None


class AlertPublic(BaseModel):
    id: int | None = None
    zone: str
    alert_type: str
    severity: str
    title: str
    description: str
    supporting_signals: list[str] | None = None
    timestamp: datetime
    metadata: dict[str, Any] | None = None
