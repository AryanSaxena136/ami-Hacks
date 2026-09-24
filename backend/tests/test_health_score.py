from app.services.health_score import compute_zone_health_score


def test_health_score_reduces_for_disruption_case():
    metrics = {
        "zone": "Vaishali Nagar",
        "rainfall": 42,
        "traffic": 81,
        "incident_reports": 17,
        "anomaly_count": 3,
    }
    score = compute_zone_health_score(metrics)

    assert 0 <= score["score"] <= 100
    assert score["status"] in {"critical", "elevated", "moderate", "good", "healthy"}
    assert score["score"] < 70
