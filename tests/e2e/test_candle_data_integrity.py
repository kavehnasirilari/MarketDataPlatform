import requests


BASE_URL = "http://localhost:8000"
CANDLES_URL = f"{BASE_URL}/candles/binance/futures/BTC-USDT/1m"


def get_candles():
    response = requests.get(CANDLES_URL, timeout=10)

    assert response.status_code == 200

    body = response.json()

    assert body["type"] == "success"
    assert body["message"] is None
    assert isinstance(body["data"], list)
    assert len(body["data"]) > 0

    return body["data"]


def test_candles_have_no_null_required_fields():
    candles = get_candles()

    required_fields = [
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    for candle in candles:
        for field in required_fields:
            assert field in candle
            assert candle[field] is not None


def test_candles_have_valid_ohlc_relationships():
    candles = get_candles()

    for candle in candles:
        assert candle["high"] >= candle["open"]
        assert candle["high"] >= candle["close"]
        assert candle["high"] >= candle["low"]

        assert candle["low"] <= candle["open"]
        assert candle["low"] <= candle["close"]
        assert candle["low"] <= candle["high"]


def test_candles_have_non_negative_volume():
    candles = get_candles()

    for candle in candles:
        assert candle["volume"] >= 0


def test_candle_timestamps_are_unique():
    candles = get_candles()

    timestamps = [candle["timestamp"] for candle in candles]

    assert len(timestamps) == len(set(timestamps))


def test_candle_timestamps_are_sorted_ascending():
    candles = get_candles()

    timestamps = [candle["timestamp"] for candle in candles]

    assert timestamps == sorted(timestamps)