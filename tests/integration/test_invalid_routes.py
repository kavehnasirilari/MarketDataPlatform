from fastapi.testclient import TestClient

from api_service.app.api.main import app


client = TestClient(app)


def test_unknown_route_returns_404():
    response = client.get("/unknown-route")

    assert response.status_code == 404