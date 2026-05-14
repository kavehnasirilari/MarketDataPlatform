import os
import pytest
import requests


@pytest.mark.skipif(
    not os.getenv("PUBLIC_API_BASE_URL"),
    reason="PUBLIC_API_BASE_URL is not set"
)
def test_public_api_metadata_endpoint_is_reachable():
    base_url = os.getenv("PUBLIC_API_BASE_URL")

    response = requests.get(f"{base_url}/metadata", timeout=10)

    assert response.status_code == 200

    body = response.json()

    assert "type" in body
    assert "message" in body
    assert "data" in body