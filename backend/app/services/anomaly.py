from __future__ import annotations

from datetime import datetime
from typing import Any


def _read_value(event: dict[str, Any]) -> float:
    return float(event.get("value", 0) or 0)


def detect_anomalies(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    anomalies: list[dict[str, Any]] = []
    for event in events:
        source = event.get("source")
        data_type = event.get("data_type")
        zone = event.get("zone", "Unknown")
        value = _read_value(event)
        timestamp = event.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        if timestamp is None:
            timestamp = datetime.utcnow()

        if source == "weather" and data_type == "rainfall":
            if value < 10:
                continue
            if value >= 30:
                anomalies.append(
                    {
                        "zone": zone,
                        "type": "high_rainfall",
                        "severity": "high",
                        "message": "Rainfall is significantly elevated.",
                        "timestamp": timestamp.isoformat(),
                    }
                )
        elif source == "traffic" and data_type == "congestion":
            if value >= 70:
                anomalies.append(
                    {
                        "zone": zone,
                        "type": "high_traffic",
                        "severity": "high",
                        "message": "Traffic congestion is unusually high.",
                        "timestamp": timestamp.isoformat(),
                    }
                )
        elif source == "incident" and value >= 10:
            anomalies.append(
                {
                    "zone": zone,
                    "type": "incident_spike",
                    "severity": "medium",
                    "message": "Incident reports are above the normal baseline.",
                    "timestamp": timestamp.isoformat(),
                }
            )
    return anomalies
