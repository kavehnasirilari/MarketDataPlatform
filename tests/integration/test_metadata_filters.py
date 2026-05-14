from fastapi.testclient import TestClient

from api_service.app.api.main import app


client = TestClient(app)


def test_metadata_filter_by_exchange():
    response = client.get("/metadata?exchange=binance")

    assert response.status_code == 200

    body = response.json()
    exchanges = body["data"]["exchanges"]

    assert body["type"] == "success"
    assert len(exchanges) > 0

    for exchange in exchanges:
        assert exchange["name"] == "binance"


def test_metadata_filter_by_market():
    response = client.get("/metadata?market=futures")

    assert response.status_code == 200

    body = response.json()
    exchanges = body["data"]["exchanges"]

    assert body["type"] == "success"
    assert len(exchanges) > 0

    for exchange in exchanges:
        for market in exchange["markets"]:
            assert market["market_type"] == "futures"


def test_metadata_filter_by_symbol():
    response = client.get("/metadata?symbol=BTC-USDT")

    assert response.status_code == 200

    body = response.json()
    exchanges = body["data"]["exchanges"]

    assert body["type"] == "success"
    assert len(exchanges) > 0

    for exchange in exchanges:
        for market in exchange["markets"]:
            assert market["symbol"] == "BTC-USDT"


def test_metadata_filter_by_interval():
    response = client.get("/metadata?interval=1m")

    assert response.status_code == 200

    body = response.json()
    exchanges = body["data"]["exchanges"]

    assert body["type"] == "success"
    assert len(exchanges) > 0

    for exchange in exchanges:
        for market in exchange["markets"]:
            assert "1m" in market["intervals"]