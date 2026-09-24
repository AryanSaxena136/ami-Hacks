from __future__ import annotations

from datetime import datetime
from typing import Any


def _normalize_common(payload: dict[str, Any], *, source: str, data_type: str) -> dict[str, Any]:
    value = float(payload.get("value", 0))
    zone = payload.get("zone") or "Unknown"
    timestamp = payload.get("timestamp")
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp)
    if timestamp is None:
        timestamp = datetime.utcnow()

    data = {
        "source": source,
        "data_type": data_type,
        "value": value,
        "unit": payload.get("unit"),
        "zone": zone,
        "latitude": payload.get("latitude"),
        "longitude": payload.get("longitude"),
        "timestamp": timestamp,
        "metadata": payload.get("metadata") or {},
    }
    if data["source"] == "weather" and data["data_type"] == "rainfall":
        if value < 10:
            data["severity"] = "normal"
        elif value < 30:
            data["severity"] = "moderate"
        else:
            data["severity"] = "high"
    elif data["source"] == "traffic" and data["data_type"] == "congestion":
        if value < 50:
            data["severity"] = "normal"
        elif value < 70:
            data["severity"] = "elevated"
        else:
            data["severity"] = "high"
    elif data["source"] == "incident":
        if value < 5:
            data["severity"] = "low"
        elif value < 20:
            data["severity"] = "medium"
        else:
            data["severity"] = "high"
    else:
        data["severity"] = payload.get("severity")
    return data


def normalize_weather(payload: dict[str, Any]) -> dict[str, Any]:
    return _normalize_common(payload, source="weather", data_type=payload.get("data_type", "rainfall"))


def normalize_traffic(payload: dict[str, Any]) -> dict[str, Any]:
    return _normalize_common(payload, source="traffic", data_type=payload.get("data_type", "congestion"))


def normalize_incident(payload: dict[str, Any]) -> dict[str, Any]:
    return _normalize_common(payload, source="incident", data_type=payload.get("data_type", "waterlogging"))


def normalize_civic_event(payload: dict[str, Any]) -> dict[str, Any]:
    source = payload.get("source", "")
    if source == "weather":
        return normalize_weather(payload)
    if source == "traffic":
        return normalize_traffic(payload)
    if source == "incident":
        return normalize_incident(payload)
    raise ValueError(f"Unsupported data source: {source}")
