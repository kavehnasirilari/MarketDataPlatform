import requests


BASE_URL = "http://localhost:8000"


def test_metadata_response_contract():
    response = requests.get(f"{BASE_URL}/metadata", timeout=10)

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)
    assert body["type"] == "success"
    assert body["message"] is None
    assert isinstance(body["data"], dict)

    assert "exchanges" in body["data"]
    assert isinstance(body["data"]["exchanges"], list)
    assert len(body["data"]["exchanges"]) > 0

    exchange = body["data"]["exchanges"][0]

    assert "name" in exchange
    assert "markets" in exchange
    assert isinstance(exchange["name"], str)
    assert isinstance(exchange["markets"], list)


def test_candles_response_contract():
    response = requests.get(
        f"{BASE_URL}/candles/hyperliquid/futures/ETH-USDC/1m",
        timeout=10,
    )

    assert response.status_code == 200

    body = response.json()
    # print(body)

    assert isinstance(body, dict)
    assert body["type"] == "success"
    assert body["message"] is None
    assert isinstance(body["data"], list)
    assert len(body["data"]) > 0

    candle = body["data"][0]

    required_fields = [
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    for field in required_fields:
        assert field in candle

    assert isinstance(candle["timestamp"], int)

    for field in ["open", "high", "low", "close", "volume"]:
        assert isinstance(candle[field], (int, float))


def test_candles_are_sorted_by_timestamp_ascending():
    response = requests.get(
        f"{BASE_URL}/candles/hyperliquid/futures/ETH-USDC/1m",
        timeout=10,
    )

    assert response.status_code == 200

    body = response.json()
    candles = body["data"]

    timestamps = [candle["timestamp"] for candle in candles]

    assert timestamps == sorted(timestamps)



    