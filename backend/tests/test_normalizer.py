from app.services.normalizer import normalize_incident, normalize_traffic, normalize_weather


def test_normalize_weather():
    payload = {
        "source": "weather",
        "data_type": "rainfall",
        "value": 42,
        "unit": "mm",
        "zone": "Vaishali Nagar",
        "latitude": 26.9124,
        "longitude": 75.7873,
        "timestamp": "2026-09-24T14:20:00",
    }
    result = normalize_weather(payload)
    assert result["source"] == "weather"
    assert result["data_type"] == "rainfall"
    assert result["value"] == 42
    assert result["severity"] == "high"


def test_normalize_traffic_and_incident():
    traffic = normalize_traffic({
        "source": "traffic",
        "data_type": "congestion",
        "value": 81,
        "unit": "percent",
        "zone": "Vaishali Nagar",
        "latitude": 26.9124,
        "longitude": 75.7873,
        "timestamp": "2026-09-24T14:21:00",
    })
    incident = normalize_incident({
        "source": "incident",
        "data_type": "waterlogging",
        "value": 17,
        "unit": "reports",
        "zone": "Vaishali Nagar",
        "latitude": 26.9124,
        "longitude": 75.7873,
        "timestamp": "2026-09-24T14:22:00",
    })

    assert traffic["severity"] == "high"
    assert incident["severity"] == "medium"
    assert incident["data_type"] == "waterlogging"
