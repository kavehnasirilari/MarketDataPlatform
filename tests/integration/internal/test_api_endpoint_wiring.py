from types import SimpleNamespace
from fastapi.testclient import TestClient
import api_service.app.api.main as api_main


class FakeOrchestrator:
    def __init__(self):
        self.calls = []

    def handle_request(self, request, route=None, payload=None):
        self.calls.append(
            {
                "path": request.url.path,
                "method": request.method,
                "route": route,
                "payload": payload,
            }
        )

        return {
            "type": "success",
            "message": None,
            "data": {
                "route": route,
                "payload": payload,
            },
        }

def test_metadata_endpoint_passes_expected_route_and_payload(monkeypatch):
    fake_orchestrator = FakeOrchestrator()

    monkeypatch.setattr(api_main, "orchestrator", fake_orchestrator)

    client = TestClient(api_main.app)

    response = client.get(
        "/metadata?exchange=binance&market=futures&symbol=BTC-USDT&interval=1m"
    )

    assert response.status_code == 200

    assert fake_orchestrator.calls == [
        {
            "path": "/metadata",
            "method": "GET",
            "route": "get_metadata",
            "payload": {
                "exchange": "binance",
                "market": "futures",
                "symbol": "BTC-USDT",
                "interval": "1m",
            },
        }
    ]

def test_metadata_endpoint_uses_none_for_missing_optional_filters(monkeypatch):
    fake_orchestrator = FakeOrchestrator()

    monkeypatch.setattr(api_main, "orchestrator", fake_orchestrator)

    client = TestClient(api_main.app)

    response = client.get("/metadata")

    assert response.status_code == 200

    assert fake_orchestrator.calls[0]["route"] == "get_metadata"
    assert fake_orchestrator.calls[0]["payload"] == {
        "exchange": None,
        "market": None,
        "symbol": None,
        "interval": None,
    }

def test_candles_endpoint_passes_expected_route_and_payload(monkeypatch):
    fake_orchestrator = FakeOrchestrator()

    monkeypatch.setattr(api_main, "orchestrator", fake_orchestrator)

    client = TestClient(api_main.app)

    response = client.get("/candles/hyperliquid/futures/ETH-USDC/1m?limit=50")

    assert response.status_code == 200

    assert fake_orchestrator.calls == [
        {
            "path": "/candles/hyperliquid/futures/ETH-USDC/1m",
            "method": "GET",
            "route": "get_candles",
            "payload": {
                "exchange": "hyperliquid",
                "market": "futures",
                "symbol": "ETH-USDC",
                "interval": "1m",
                "limit": 50,
            },
        }
    ]

def test_candles_endpoint_uses_default_limit(monkeypatch):
    fake_orchestrator = FakeOrchestrator()

    monkeypatch.setattr(api_main, "orchestrator", fake_orchestrator)

    client = TestClient(api_main.app)

    response = client.get("/candles/hyperliquid/futures/ETH-USDC/1m")

    assert response.status_code == 200

    assert fake_orchestrator.calls[0]["payload"]["limit"] == 100

def test_health_endpoint_calls_orchestrator_without_route_or_payload(monkeypatch):
    fake_orchestrator = FakeOrchestrator()

    monkeypatch.setattr(api_main, "orchestrator", fake_orchestrator)

    client = TestClient(api_main.app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "type": "success",
        "message": None,
        "data": {
            "status": "ok",
        },
    }
    assert fake_orchestrator.calls == []

def test_candles_endpoint_rejects_invalid_limit_before_orchestrator(monkeypatch):
    fake_orchestrator = FakeOrchestrator()

    monkeypatch.setattr(api_main, "orchestrator", fake_orchestrator)

    client = TestClient(api_main.app)

    response = client.get("/candles/hyperliquid/futures/ETH-USDC/1m?limit=not-number")

    assert response.status_code == 422
    assert fake_orchestrator.calls == []
