from __future__ import annotations

from datetime import datetime
from random import uniform

ZONES = {
    "Vaishali Nagar": {"latitude": 26.9124, "longitude": 75.7873},
    "Malviya Nagar": {"latitude": 26.8540, "longitude": 75.8070},
    "Mansarovar": {"latitude": 26.8994, "longitude": 75.7755},
    "C-Scheme": {"latitude": 26.9122, "longitude": 75.7994},
    "Jagatpura": {"latitude": 26.8140, "longitude": 75.8233},
}


def generate_weather_feed(zone_name: str | None = None, disruption: bool = False) -> dict:
    zone = zone_name or "Vaishali Nagar"
    coords = ZONES.get(zone, ZONES["Vaishali Nagar"])
    rainfall = 42 if disruption else round(uniform(2, 18), 1)
    if not disruption:
        rainfall = max(0, min(25, rainfall))
    return {
        "source": "weather",
        "data_type": "rainfall",
        "value": rainfall,
        "unit": "mm",
        "zone": zone,
        "latitude": coords["latitude"],
        "longitude": coords["longitude"],
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": {"condition": "heavy rain" if disruption else "light to moderate rain"},
    }


def generate_weather_batch(disruption: bool = False) -> list[dict]:
    return [generate_weather_feed(zone_name=zone, disruption=disruption) for zone in ZONES]
