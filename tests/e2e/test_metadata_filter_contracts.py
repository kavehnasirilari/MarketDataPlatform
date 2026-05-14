import requests


BASE_URL = "http://localhost:8000"


def test_metadata_filter_by_exchange_returns_only_that_exchange():
    response = requests.get(
        f"{BASE_URL}/metadata?exchange=binance",
        timeout=10,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["type"] == "success"
    assert body["message"] is None
    assert "exchanges" in body["data"]

    exchanges = body["data"]["exchanges"]

    assert len(exchanges) > 0

    for exchange in exchanges:
        assert exchange["name"] == "binance"

def test_metadata_filter_by_market_type_returns_only_that_market_type():
    response = requests.get(
        f"{BASE_URL}/metadata?market=futures",
        timeout=10,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["type"] == "success"
    assert body["message"] is None

    exchanges = body["data"]["exchanges"]

    assert len(exchanges) > 0

    for exchange in exchanges:
        for market in exchange["markets"]:
            assert market["market_type"] == "futures"

def test_metadata_filter_by_symbol_returns_only_that_symbol():
    response = requests.get(
        f"{BASE_URL}/metadata?symbol=BTC-USDT",
        timeout=10,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["type"] == "success"
    assert body["message"] is None

    exchanges = body["data"]["exchanges"]

    assert len(exchanges) > 0

    for exchange in exchanges:
        for market in exchange["markets"]:
            assert market["symbol"] == "BTC-USDT"

def test_metadata_filter_by_interval_returns_only_markets_supporting_that_interval():
    response = requests.get(
        f"{BASE_URL}/metadata?interval=1m",
        timeout=10,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["type"] == "success"
    assert body["message"] is None

    exchanges = body["data"]["exchanges"]

    assert len(exchanges) > 0

    for exchange in exchanges:
        for market in exchange["markets"]:
            assert "1m" in market["intervals"]