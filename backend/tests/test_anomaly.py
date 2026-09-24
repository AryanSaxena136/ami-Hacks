from app.services.anomaly import detect_anomalies


def test_rainfall_and_traffic_anomalies_for_disruption_case():
    events = [
        {
            "source": "weather",
            "data_type": "rainfall",
            "value": 42,
            "unit": "mm",
            "zone": "Vaishali Nagar",
            "latitude": 26.9124,
            "longitude": 75.7873,
            "timestamp": "2026-09-24T14:20:00",
        },
        {
            "source": "traffic",
            "data_type": "congestion",
            "value": 81,
            "unit": "percent",
            "zone": "Vaishali Nagar",
            "latitude": 26.9124,
            "longitude": 75.7873,
            "timestamp": "2026-09-24T14:21:00",
        },
    ]

    anomalies = detect_anomalies(events)
    types = {item["type"] for item in anomalies}

    assert "high_rainfall" in types
    assert "high_traffic" in types
