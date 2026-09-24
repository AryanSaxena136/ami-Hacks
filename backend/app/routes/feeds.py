from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.civic_data import CivicData
from app.services.ingestion import fetch_latest_data, simulate_disruption_batch

router = APIRouter(prefix="/api", tags=["feeds"])


@router.post("/ingest/simulate", summary="Generate one simulated civic data batch")
def ingest_simulate(disruption: bool = True) -> dict[str, object]:
    events = simulate_disruption_batch(disruption=disruption)
    return {"status": "ok", "count": len(events), "message": "Simulated civic batch ingested."}


@router.get("/data/latest", summary="Return latest civic data")
def latest_data(limit: int = 50) -> dict[str, object]:
    if limit <= 0:
        raise HTTPException(status_code=400, detail="limit must be greater than 0")
    return {"count": limit, "items": fetch_latest_data(limit)}


@router.get("/feeds/status", summary="Return feed health")
def feed_status(db: Session = Depends(get_db)) -> dict[str, object]:
    now = datetime.utcnow()
    status: dict[str, object] = {}
    for source in ["weather", "traffic", "incidents"]:
        latest = (
            db.query(CivicData)
            .filter(CivicData.source == source)
            .order_by(CivicData.timestamp.desc())
            .first()
        )
        if latest:
            status[source] = {"status": "online", "last_updated": latest.timestamp.isoformat()}
        else:
            status[source] = {"status": "offline", "last_updated": now.isoformat()}
    return status
