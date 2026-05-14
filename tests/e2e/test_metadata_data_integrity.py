import requests


BASE_URL = "http://localhost:8000"


def get_metadata():
    response = requests.get(f"{BASE_URL}/metadata", timeout=10)

    assert response.status_code == 200

    body = response.json()

    assert body["type"] == "success"
    assert body["message"] is None
    assert isinstance(body["data"], dict)
    assert "exchanges" in body["data"]
    assert isinstance(body["data"]["exchanges"], list)
    assert len(body["data"]["exchanges"]) > 0

    return body["data"]["exchanges"]


def test_exchange_names_are_not_empty():
    exchanges = get_metadata()

    for exchange in exchanges:
        assert isinstance(exchange["name"], str)
        assert exchange["name"].strip()


def test_markets_have_required_non_empty_fields():
    exchanges = get_metadata()

    required_fields = [
        "symbol",
        "exchange_symbol",
        "market_type",
        "intervals",
    ]

    for exchange in exchanges:
        for market in exchange["markets"]:
            for field in required_fields:
                assert field in market
                assert market[field] is not None

            assert isinstance(market["symbol"], str)
            assert market["symbol"].strip()

            assert isinstance(market["exchange_symbol"], str)
            assert market["exchange_symbol"].strip()

            assert market["market_type"] in ["spot", "futures"]

            assert isinstance(market["intervals"], list)
            assert len(market["intervals"]) > 0


def test_market_intervals_are_unique_and_sorted():
    exchanges = get_metadata()

    for exchange in exchanges:
        for market in exchange["markets"]:
            intervals = market["intervals"]

            assert len(intervals) == len(set(intervals))
            assert intervals == sorted(intervals)


def test_market_identity_is_unique_per_exchange():
    exchanges = get_metadata()

    for exchange in exchanges:
        identities = []

        for market in exchange["markets"]:
            identity = (
                market["symbol"],
                market["exchange_symbol"],
                market["market_type"],
            )
            identities.append(identity)

        assert len(identities) == len(set(identities))