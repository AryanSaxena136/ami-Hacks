from __future__ import annotations

from datetime import datetime
from random import randint, uniform

ZONES = {
    "Vaishali Nagar": {"latitude": 26.9124, "longitude": 75.7873},
    "Malviya Nagar": {"latitude": 26.8540, "longitude": 75.8070},
    "Mansarovar": {"latitude": 26.8994, "longitude": 75.7755},
    "C-Scheme": {"latitude": 26.9122, "longitude": 75.7994},
    "Jagatpura": {"latitude": 26.8140, "longitude": 75.8233},
}


def generate_traffic_feed(zone_name: str | None = None, disruption: bool = False) -> dict:
    zone = zone_name or "Vaishali Nagar"
    coords = ZONES.get(zone, ZONES["Vaishali Nagar"])
    congestion = 81 if disruption else randint(20, 68)
    if not disruption:
        congestion = max(15, min(90, congestion))
    return {
        "source": "traffic",
        "data_type": "congestion",
        "value": congestion,
        "unit": "percent",
        "zone": zone,
        "latitude": coords["latitude"],
        "longitude": coords["longitude"],
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": {"vehicle_flow": "high" if disruption else "moderate"},
    }


def generate_traffic_batch(disruption: bool = False) -> list[dict]:
    return [generate_traffic_feed(zone_name=zone, disruption=disruption) for zone in ZONES]
