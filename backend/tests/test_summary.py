import httpx

from app.services.summary import generate_summary


def test_generate_summary_uses_llm_when_configured(monkeypatch):
    observed = {}

    class FakeResponse:
        status_code = 200

        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": "LLM-generated summary of the civic disruption."}}]}

    def fake_post(url, headers=None, json=None, **kwargs):
        observed["url"] = url
        observed["headers"] = headers
        observed["json"] = json
        return FakeResponse()

    monkeypatch.setenv("LLM_API_KEY", "test-key")
    monkeypatch.setenv("LLM_MODEL", "gpt-4o-mini")
    monkeypatch.setenv("LLM_BASE_URL", "https://api.openai.com/v1")
    monkeypatch.setattr(httpx, "post", fake_post)

    result = generate_summary({
        "zone": "Vaishali Nagar",
        "rainfall": 45,
        "traffic": 80,
        "incident_reports": 12,
    })

    assert result == "LLM-generated summary of the civic disruption."
    assert observed["headers"]["Authorization"] == "Bearer test-key"
    assert "messages" in observed["json"]


def test_generate_summary_uses_grok_when_configured(monkeypatch):
    observed = {}

    class FakeResponse:
        status_code = 200

        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": "Grok generated the civic operations summary."}}]}

    def fake_post(url, headers=None, json=None, **kwargs):
        observed["url"] = url
        observed["headers"] = headers
        observed["json"] = json
        return FakeResponse()

    monkeypatch.setenv("GROK_API_KEY", "grok-key")
    monkeypatch.setenv("GROK_MODEL", "grok-2-latest")
    monkeypatch.setenv("GROK_BASE_URL", "https://api.x.ai/v1")
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.setattr(httpx, "post", fake_post)

    result = generate_summary({
        "zone": "Malviya Nagar",
        "rainfall": 28,
        "traffic": 72,
        "incident_reports": 7,
    })

    assert result == "Grok generated the civic operations summary."
    assert observed["headers"]["Authorization"] == "Bearer grok-key"
    assert observed["url"] == "https://api.x.ai/v1/chat/completions"
    assert observed["json"]["model"] == "grok-2-latest"
