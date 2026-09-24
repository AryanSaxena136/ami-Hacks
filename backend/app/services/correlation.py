from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def detect_possible_correlations(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_zone: dict[str, list[dict[str, Any]]] = {}
    for event in events:
        by_zone.setdefault(event.get("zone", "Unknown"), []).append(event)

    alerts: list[dict[str, Any]] = []
    for zone, zone_events in by_zone.items():
        rainfall = max(
            (e.get("value", 0) for e in zone_events if e.get("source") == "weather" and e.get("data_type") == "rainfall"),
            default=0,
        )
        congestion = max(
            (e.get("value", 0) for e in zone_events if e.get("source") == "traffic" and e.get("data_type") == "congestion"),
            default=0,
        )
        waterlogging = max(
            (e.get("value", 0) for e in zone_events if e.get("source") == "incident" and e.get("data_type") == "waterlogging"),
            default=0,
        )

        if rainfall > 30 and congestion > 70 and waterlogging > 10:
            alerts.append(
                {
                    "zone": zone,
                    "alert_type": "possible_correlation",
                    "severity": "high",
                    "title": "Possible co-occurring civic disruption",
                    "description": (
                        "Possible correlation: heavy rainfall is currently coinciding with increased traffic "
                        "congestion and waterlogging reports in this zone. This does not prove causation; "
                        "it indicates co-occurring signals that may require attention."
                    ),
                    "supporting_signals": [
                        f"rainfall={rainfall}",
                        f"congestion={congestion}",
                        f"waterlogging={waterlogging}",
                    ],
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            )
    return alerts
