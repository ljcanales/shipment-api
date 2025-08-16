from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_tracking_rejects_invalid_courier():
    response = client.get("/api/v1/shipments/123", params={"courier": "invalid"})
    assert response.status_code == 422


def test_get_tracking_accepts_valid_courier():
    response = client.get("/api/v1/shipments/123", params={"courier": "stub"})
    assert response.status_code == 200
    assert response.json()["courier"] == "stub"
