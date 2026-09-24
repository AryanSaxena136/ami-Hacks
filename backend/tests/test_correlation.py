from app.services.correlation import detect_possible_correlations


def test_correlation_detection_for_coinciding_signals():
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
        {
            "source": "incident",
            "data_type": "waterlogging",
            "value": 17,
            "unit": "reports",
            "zone": "Vaishali Nagar",
            "latitude": 26.9124,
            "longitude": 75.7873,
            "timestamp": "2026-09-24T14:22:00",
        },
    ]

    correlations = detect_possible_correlations(events)
    assert len(correlations) >= 1
    assert correlations[0]["alert_type"] == "possible_correlation"
    assert "possible correlation" in correlations[0]["description"].lower()
