from __future__ import annotations

from typing import Any


def compute_zone_health_score(metrics: dict[str, Any]) -> dict[str, Any]:
    zone = metrics.get("zone", "Unknown")
    rainfall = float(metrics.get("rainfall", 0) or 0)
    traffic = float(metrics.get("traffic", 0) or 0)
    incident_reports = float(metrics.get("incident_reports", 0) or 0)
    anomaly_count = int(metrics.get("anomaly_count", 0) or 0)

    score = 100
    score -= rainfall * 0.45
    score -= traffic * 0.25
    score -= incident_reports * 0.8
    score -= anomaly_count * 8

    if score < 0:
        score = 0
    if score > 100:
        score = 100

    score = int(round(score))
    if score >= 80:
        status = "healthy"
    elif score >= 60:
        status = "moderate"
    elif score >= 40:
        status = "elevated"
    elif score >= 20:
        status = "critical"
    else:
        status = "critical"

    return {"zone": zone, "score": score, "status": status}
