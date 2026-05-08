from fastapi.testclient import TestClient

from api_service.app.api.main import app


client = TestClient(app)


def test_metadata_endpoint_returns_success_contract():
    
    response = client.get("/metadata")

    assert response.status_code == 200

    body  = response.json()
   
    assert body["type"] == "success"
    assert body["message"] is None
    assert "data" in body
    assert "exchanges" in body["data"]

    exchanges = body["data"]["exchanges"]

    assert isinstance(exchanges, list)
    assert len(exchanges) > 0


def test_metadata_endpoint_returns_exchange_market_structure():
    
    response = client.get("/metadata")

    assert response.status_code == 200

    body = response.json()
    exchanges = body["data"]["exchanges"]

    first_exchange = exchanges[0]

    assert "name" in first_exchange
    assert "markets" in first_exchange
    assert isinstance(first_exchange["markets"], list)
    assert len(first_exchange["markets"]) > 0

    first_market = first_exchange["markets"][0]

    assert "symbol" in first_market
    assert "exchange_symbol" in first_market
    assert "market_type" in first_market
    assert "intervals" in first_market
    assert isinstance(first_market["intervals"], list)
    assert len(first_market["intervals"]) > 0