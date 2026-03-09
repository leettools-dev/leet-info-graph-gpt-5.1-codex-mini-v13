from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_generate_infographic_returns_spec():
    response = client.post("/api/v1/infographics/generate", json={"prompt": "What's new in AI?"})
    assert response.status_code == 200
    assert "image/png" in response.headers["content-type"]
