from fastapi.testclient import TestClient

from api_service.app.api.main import app
import pytest

client = TestClient(app)


def test_metadata_returns_success_empty_result_when_no_rows_match():
    response = client.get(
        "/metadata?symbol=THIS-SYMBOL-SHOULD-NOT-EXIST"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["type"] == "error"
    assert body["message"] is None
    assert body["data"] is None