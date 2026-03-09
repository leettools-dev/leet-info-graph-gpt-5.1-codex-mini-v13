from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_generate_infographic_returns_structured_result():
    response = client.post("/api/v1/infographics/generate", json={"prompt": "What's new in AI?"})
    assert response.status_code == 200
    payload = response.json()
    assert "spec" in payload
    assert "sources" in payload
    assert payload["confidence_note"].startswith("Confidence:")
    assert payload["provenance"].get("sources_fetched_at")
    assert payload["image_url"].startswith("data:image/png;base64,")
