# CityPulse Backend

CityPulse is a lightweight hackathon MVP that combines simulated civic data streams into a live civic health dashboard.

## Overview

The backend ingests three signals:
- weather
- traffic
- civic incidents

It normalizes each feed into a common schema, stores the raw events in SQLite, checks for anomalies, detects possible co-occurring patterns, and calculates a zone-level civic health score.

## Architecture

- FastAPI serves the API and Swagger docs
- SQLAlchemy 2.x manages SQLite persistence
- Pydantic v2 validates the request and response schemas
- feeder modules generate realistic Jaipur zone data
- rule-based anomaly and correlation engines produce explainable alerts
- the dashboard endpoint aggregates all of the above for a React frontend

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x
- Pydantic v2
- SQLite
- Uvicorn
- pytest

## Project Structure

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── civic_data.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── feeds.py
│   │   ├── alerts.py
│   │   └── dashboard.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── civic.py
│   │   └── dashboard.py
│   ├── services/
│   │   ├── anomaly.py
│   │   ├── correlation.py
│   │   ├── health_score.py
│   │   ├── ingestion.py
│   │   ├── normalizer.py
│   │   └── summary.py
│   └── feeds/
│       ├── weather.py
│       ├── traffic.py
│       └── incidents.py
├── tests/
│   ├── test_anomaly.py
│   ├── test_correlation.py
│   ├── test_health_score.py
│   └── test_normalizer.py
├── .env.example
├── requirements.txt
├── README.md
└── citypulse.db
```

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the backend

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

The API will be available at:
- http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- GET /
- GET /api/health
- POST /api/ingest/simulate
- GET /api/data/latest
- GET /api/feeds/status
- GET /api/alerts
- GET /api/alerts/{zone}
- GET /api/dashboard

## Example API responses

### Dashboard summary

```json
{
  "city_score": 68,
  "status": "moderate",
  "zones": [
    {
      "zone": "Vaishali Nagar",
      "score": 52,
      "status": "elevated",
      "latitude": 26.9124,
      "longitude": 75.7873
    }
  ],
  "latest_signals": [],
  "active_alerts": [],
  "summary": "Heavy rainfall is currently coinciding with high traffic congestion and increased waterlogging reports in Vaishali Nagar. Residents may experience localized travel disruption.",
  "last_updated": "2026-09-24T14:22:00"
}
```

### Alert example

```json
{
  "zone": "Vaishali Nagar",
  "alert_type": "possible_correlation",
  "severity": "high",
  "title": "Possible co-occurring civic disruption",
  "description": "Heavy rainfall is currently coinciding with increased traffic congestion and waterlogging reports in this zone. This may indicate a co-occurring civic disruption.",
  "supporting_signals": ["rainfall=42", "congestion=81", "waterlogging=17"],
  "timestamp": "2026-09-24T14:22:00"
}
```

## Trigger the simulated disruption

The backend creates a disruption when `POST /api/ingest/simulate` is called.

```bash
curl -X POST "http://localhost:8000/api/ingest/simulate?disruption=true"
```

This generates weather, traffic, and incident values similar to:
- rainfall = 42
- traffic = 81
- waterlogging = 17

## How the anomaly and correlation engine works

The implementation is intentionally simple and explainable:

1. Each feed is normalized to a common civic event format.
2. Rule-based thresholds flag high rainfall, high congestion, and abnormal incident counts.
3. The correlation service checks whether multiple signals co-occur in the same zone within a rolling time window.
4. The system never says a signal caused another; it uses language such as "currently coinciding with" and "possible correlation".
5. The city health score blends rainfall, traffic, incidents, and anomaly activity into a composite 0-100 indicator.

## Notes for a hackathon

- The service is intentionally easy to understand and replace with real API integrations later.
- Database initialization happens automatically on startup.
- Feed failures are isolated so one data source can fail without crashing the dashboard.
