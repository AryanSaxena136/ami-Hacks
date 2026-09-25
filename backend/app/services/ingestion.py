from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.feeds.incidents import generate_incident_batch
from app.feeds.traffic import generate_traffic_batch
from app.feeds.weather import generate_weather_batch
from app.models.civic_data import AlertRecord, CivicData
from app.services.anomaly import detect_anomalies
from app.services.correlation import detect_possible_correlations
from app.services.normalizer import normalize_civic_event
from app.services.summary import generate_summary


def _event_to_record(event: dict[str, Any]) -> CivicData:
    normalized = normalize_civic_event(event)
    return CivicData(
        source=normalized["source"],
        data_type=normalized["data_type"],
        value=float(normalized["value"]),
        unit=normalized.get("unit"),
        severity=normalized.get("severity"),
        zone=normalized["zone"],
        latitude=normalized.get("latitude"),
        longitude=normalized.get("longitude"),
        timestamp=normalized["timestamp"],
        payload_metadata=json.dumps(normalized.get("metadata") or {}),
    )


def ingest_batch(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    saved: list[dict[str, Any]] = []
    db: Session = SessionLocal()
    try:
        for event in events:
            db.add(_event_to_record(event))
            saved.append(event)
        db.commit()
    finally:
        db.close()

    anomalies = detect_anomalies([normalize_civic_event(event) for event in events])
    for anomaly in anomalies:
        db = SessionLocal()
        try:
            db.add(
                AlertRecord(
                    zone=anomaly["zone"],
                    alert_type=anomaly["type"],
                    severity=anomaly["severity"],
                    title=anomaly["type"].replace("_", " ").title(),
                    description=anomaly["message"],
                    supporting_signals=anomaly["type"],
                    timestamp=datetime.fromisoformat(anomaly["timestamp"]),
                    payload_metadata=json.dumps({"source": "anomaly"}),
                )
            )
            db.commit()
        finally:
            db.close()

    correlations = detect_possible_correlations([normalize_civic_event(event) for event in events])
    for correlation in correlations:
        db = SessionLocal()
        try:
            db.add(
                AlertRecord(
                    zone=correlation["zone"],
                    alert_type=correlation["alert_type"],
                    severity=correlation["severity"],
                    title=correlation["title"],
                    description=correlation["description"],
                    supporting_signals=",".join(correlation.get("supporting_signals", [])),
                    timestamp=datetime.fromisoformat(correlation["timestamp"]),
                    payload_metadata=json.dumps({"source": "correlation"}),
                )
            )
            db.commit()
        finally:
            db.close()

    return saved


def simulate_disruption_batch(disruption: bool = True) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for batch in (generate_weather_batch(disruption), generate_traffic_batch(disruption), generate_incident_batch(disruption)):
        events.extend(batch)
    ingest_batch(events)
    return events


def fetch_latest_data(limit: int = 50) -> list[dict[str, Any]]:
    db: Session = SessionLocal()
    try:
        records = db.query(CivicData).order_by(CivicData.timestamp.desc()).limit(limit).all()
        return [
            {
                "id": record.id,
                "source": record.source,
                "data_type": record.data_type,
                "value": record.value,
                "unit": record.unit,
                "severity": record.severity,
                "zone": record.zone,
                "latitude": record.latitude,
                "longitude": record.longitude,
                "timestamp": record.timestamp.isoformat(),
                "metadata": json.loads(record.payload_metadata) if record.payload_metadata else {},
            }
            for record in records
        ]
    finally:
        db.close()


def build_summary_for_zone(zone: str, events: list[dict[str, Any]]) -> str:
    zone_events = [event for event in events if event.get("zone") == zone]
    rainfall = max((float(e.get("value", 0) or 0) for e in zone_events if e.get("source") == "weather" and e.get("data_type") == "rainfall"), default=0)
    traffic = max((float(e.get("value", 0) or 0) for e in zone_events if e.get("source") == "traffic" and e.get("data_type") == "congestion"), default=0)
    incident_reports = max((float(e.get("value", 0) or 0) for e in zone_events if e.get("source") == "incident"), default=0)
    return generate_summary({"zone": zone, "rainfall": rainfall, "traffic": traffic, "incident_reports": incident_reports})
