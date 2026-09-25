from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.civic_data import AlertRecord, CivicData
from app.services.health_score import compute_zone_health_score
from app.services.summary import generate_summary

router = APIRouter(prefix="/api", tags=["dashboard"])

ZONES = [
    "Vaishali Nagar",
    "Malviya Nagar",
    "Mansarovar",
    "C-Scheme",
    "Jagatpura",
]


@router.get("/dashboard", summary="City dashboard summary")
def dashboard_summary(db: Session = Depends(get_db)) -> dict[str, object]:
    latest = (
        db.query(CivicData)
        .order_by(CivicData.timestamp.desc())
        .limit(100)
        .all()
    )
    if not latest:
        return {
            "city_score": 100,
            "status": "healthy",
            "zones": [],
            "latest_signals": [],
            "active_alerts": [],
            "summary": "No civic data has been ingested yet.",
            "last_updated": datetime.utcnow().isoformat(),
        }

    alerts = db.query(AlertRecord).order_by(AlertRecord.timestamp.desc()).all()
    enriched_alerts = [
        {
            "id": record.id,
            "zone": record.zone,
            "alert_type": record.alert_type,
            "severity": record.severity,
            "title": record.title,
            "description": record.description,
            "supporting_signals": record.supporting_signals.split(",") if record.supporting_signals else [],
            "timestamp": record.timestamp.isoformat(),
        }
        for record in alerts
    ]

    latest_signals = [
        {
            "source": record.source,
            "data_type": record.data_type,
            "value": record.value,
            "unit": record.unit,
            "severity": record.severity,
            "zone": record.zone,
            "latitude": record.latitude,
            "longitude": record.longitude,
            "timestamp": record.timestamp,
        }
        for record in latest
    ]

    zone_scores = []
    for zone in ZONES:
        zone_events = [event for event in latest if event.zone == zone]
        rainfall = max((float(e.value) for e in zone_events if e.source == "weather" and e.data_type == "rainfall"), default=0)
        traffic = max((float(e.value) for e in zone_events if e.source == "traffic" and e.data_type == "congestion"), default=0)
        incident_reports = max((float(e.value) for e in zone_events if e.source == "incident"), default=0)
        anomaly_count = sum(1 for alert in alerts if alert.zone == zone)
        result = compute_zone_health_score({
            "zone": zone,
            "rainfall": rainfall,
            "traffic": traffic,
            "incident_reports": incident_reports,
            "anomaly_count": anomaly_count,
        })
        coord = next((item for item in latest if item.zone == zone), None)
        zone_scores.append(
            {
                "zone": zone,
                "score": result["score"],
                "status": result["status"],
                "latitude": coord.latitude if coord else None,
                "longitude": coord.longitude if coord else None,
            }
        )

    city_score = int(sum(item["score"] for item in zone_scores) / max(len(zone_scores), 1))
    status = "healthy" if city_score >= 80 else "moderate" if city_score >= 60 else "elevated" if city_score >= 40 else "critical"
    primary_zone = max(zone_scores, key=lambda item: item["score"], default={"zone": "Unknown"})
    summary = generate_summary(
        {
            "zone": primary_zone["zone"],
            "rainfall": max((float(e.value) for e in latest if e.source == "weather" and e.data_type == "rainfall"), default=0),
            "traffic": max((float(e.value) for e in latest if e.source == "traffic" and e.data_type == "congestion"), default=0),
            "incident_reports": max((float(e.value) for e in latest if e.source == "incident"), default=0),
        }
    )

    return {
        "city_score": city_score,
        "status": status,
        "zones": zone_scores,
        "latest_signals": latest_signals[:10],
        "active_alerts": enriched_alerts,
        "summary": summary,
        "last_updated": datetime.utcnow().isoformat(),
    }
