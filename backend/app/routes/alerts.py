from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.civic_data import AlertRecord

router = APIRouter(prefix="/api", tags=["alerts"])


@router.get("/alerts", summary="List active alerts")
def list_alerts(db: Session = Depends(get_db)) -> list[dict[str, object]]:
    alerts = db.query(AlertRecord).order_by(AlertRecord.timestamp.desc()).all()
    return [
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


@router.get("/alerts/{zone}", summary="List alerts for one zone")
def alert_by_zone(zone: str, db: Session = Depends(get_db)) -> list[dict[str, object]]:
    alerts = db.query(AlertRecord).filter(AlertRecord.zone == zone).order_by(AlertRecord.timestamp.desc()).all()
    if not alerts:
        raise HTTPException(status_code=404, detail=f"No alerts found for zone: {zone}")
    return [
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
