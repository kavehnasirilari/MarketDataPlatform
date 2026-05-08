from fastapi.testclient import TestClient

from api_service.app.api.main import app


client = TestClient(app)


def test_candles_endpoint_returns_response_contract():
    response = client.get("/candles/binance/futures/BTC-USDT/1m")

    assert response.status_code == 200

    body = response.json()

    assert "type" in body
    assert "message" in body
    assert "data" in body


def test_candles_endpoint_returns_error_for_invalid_exchange():
    response = client.get("/candles/invalid/futures/BTC-USDT/1m")

    assert response.status_code in [200, 400, 404]

    body = response.json()

    assert "type" in body
    assert "message" in body    


    
def test_candles_endpoint_returns_error_for_unknown_symbol():
    response = client.get("/candles/binance/futures/UNKNOWN-COIN/1m")

    assert response.status_code == 200

    body = response.json()

    assert body["type"] == "error"
    assert body["message"] == "exchange_market not find"
    assert body["data"] is None