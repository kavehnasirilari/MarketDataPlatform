from fastapi.testclient import TestClient

from api_service.app.api.main import app


client = TestClient(app)


def assert_response_contract(body: dict):
    assert isinstance(body, dict)
    assert "type" in body
    assert "message" in body
    assert "data" in body


def assert_error_response_contract(body: dict):
    assert_response_contract(body)
    assert body["type"] == "error"
    assert isinstance(body["message"], str)
    assert body["message"]
    assert body["data"] is None


def test_candles_endpoint_returns_success_response_contract():
    response = client.get("/candles/hyperliquid/futures/ETH-USDC/1m")

    assert response.status_code == 200

    body = response.json()

    assert_response_contract(body)
    assert body["type"] == "success"
    assert body["message"] is None
    assert isinstance(body["data"], list)


def test_candles_endpoint_returns_error_for_invalid_exchange():
    response = client.get("/candles/invalid/futures/ETH-USDC/1m")

    assert response.status_code == 200

    body = response.json()

    assert_error_response_contract(body)


def test_candles_endpoint_returns_error_for_unknown_symbol():
    response = client.get("/candles/hyperliquid/futures/unnown_coin/1m")

    assert response.status_code == 200

    body = response.json()

    assert_error_response_contract(body)