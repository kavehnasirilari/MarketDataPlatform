import requests


BASE_URL = "http://localhost:8000"


def assert_error_response_contract(body: dict):
    assert isinstance(body, dict)

    assert "type" in body
    assert "message" in body
    assert "data" in body

    assert body["type"] == "error"
    assert isinstance(body["message"], str)
    assert body["message"]
    assert body["data"] is None


def test_invalid_exchange_returns_error_contract():
    response = requests.get(
        f"{BASE_URL}/candles/invalid_exchange/futures/BTC-USDT/1m",
        timeout=10,
    )

    assert response.status_code == 200

    body = response.json()

    assert_error_response_contract(body)


def test_invalid_market_type_returns_error_contract():
    response = requests.get(
        f"{BASE_URL}/candles/binance/invalid_market/BTC-USDT/1m",
        timeout=10,
    )

    assert response.status_code == 200

    body = response.json()

    assert_error_response_contract(body)


def test_invalid_symbol_returns_error_contract():
    response = requests.get(
        f"{BASE_URL}/candles/binance/futures/INVALID-SYMBOL/1m",
        timeout=10,
    )

    assert response.status_code == 200

    body = response.json()

    assert_error_response_contract(body)


def test_invalid_interval_returns_error_contract():
    response = requests.get(
        f"{BASE_URL}/candles/binance/futures/BTC-USDT/999m",
        timeout=10,
    )

    assert response.status_code == 200

    body = response.json()

    assert_error_response_contract(body)