from __future__ import annotations

from datetime import datetime
from random import randint

ZONES = {
    "Vaishali Nagar": {"latitude": 26.9124, "longitude": 75.7873},
    "Malviya Nagar": {"latitude": 26.8540, "longitude": 75.8070},
    "Mansarovar": {"latitude": 26.8994, "longitude": 75.7755},
    "C-Scheme": {"latitude": 26.9122, "longitude": 75.7994},
    "Jagatpura": {"latitude": 26.8140, "longitude": 75.8233},
}

INCIDENT_TYPES = ["waterlogging", "road_accident", "power_outage", "complaint"]


def generate_incident_feed(zone_name: str | None = None, disruption: bool = False) -> dict:
    zone = zone_name or "Vaishali Nagar"
    coords = ZONES.get(zone, ZONES["Vaishali Nagar"])
    incident_type = INCIDENT_TYPES[0] if disruption else INCIDENT_TYPES[randint(0, len(INCIDENT_TYPES) - 1)]
    value = 17 if disruption else randint(0, 7)
    return {
        "source": "incident",
        "data_type": incident_type,
        "value": value,
        "unit": "reports",
        "zone": zone,
        "latitude": coords["latitude"],
        "longitude": coords["longitude"],
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": {"incident_type": incident_type},
    }


def generate_incident_batch(disruption: bool = False) -> list[dict]:
    return [generate_incident_feed(zone_name=zone, disruption=disruption) for zone in ZONES]
