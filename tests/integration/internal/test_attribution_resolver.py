from types import SimpleNamespace

from api_service.app.attribution.http_impl import HttpAttributionResolver


class FakeHeaders(dict):
    def get(self, key, default=None):
        for existing_key, value in self.items():
            if existing_key.lower() == key.lower():
                return value
        return default


def make_request(headers=None, host="127.0.0.1", path="/metadata", method="GET"):
    return SimpleNamespace(
        headers=FakeHeaders(headers or {}),
        client=SimpleNamespace(host=host),
        url=SimpleNamespace(path=path),
        method=method,
    )


def test_resolver_uses_existing_request_id_when_header_exists():
    resolver = HttpAttributionResolver()

    request = make_request(headers={"X-Request-ID": "req-123"})

    result = resolver.resolve(request)

    assert result.request_id == "req-123"


def test_resolver_generates_request_id_when_header_is_missing():
    resolver = HttpAttributionResolver()

    request = make_request()

    result = resolver.resolve(request)

    assert isinstance(result.request_id, str)
    assert len(result.request_id) > 0


def test_resolver_uses_first_x_forwarded_for_ip_before_client_host():
    resolver = HttpAttributionResolver()

    request = make_request(
        headers={"X-Forwarded-For": "10.0.0.1, 20.0.0.1"},
        host="127.0.0.1",
    )

    result = resolver.resolve(request)

    assert result.source_ip == "10.0.0.1"
    assert result.ip_source == "x-forwarded-for"
    assert result.consumer_type == "public"
    assert result.consumer_ref == "ip:10.0.0.1"


def test_resolver_uses_x_real_ip_when_x_forwarded_for_is_missing():
    resolver = HttpAttributionResolver()

    request = make_request(
        headers={"X-Real-IP": "30.0.0.1"},
        host="127.0.0.1",
    )

    result = resolver.resolve(request)

    assert result.source_ip == "30.0.0.1"
    assert result.ip_source == "x-real-ip"
    assert result.consumer_ref == "ip:30.0.0.1"


def test_resolver_falls_back_to_direct_client_host():
    resolver = HttpAttributionResolver()

    request = make_request(host="127.0.0.1")

    result = resolver.resolve(request)

    assert result.source_ip == "127.0.0.1"
    assert result.ip_source == "direct"
    assert result.consumer_type == "public"
    assert result.consumer_ref == "ip:127.0.0.1"


def test_resolver_marks_consumer_as_registered_when_api_key_exists():
    resolver = HttpAttributionResolver()

    request = make_request(headers={"X-API-Key": "secret-key"})

    result = resolver.resolve(request)

    assert result.consumer_type == "registered"
    assert result.consumer_ref.startswith("key:")
    assert result.api_key_fingerprint is not None
    assert result.api_key_fingerprint in result.consumer_ref
    assert "secret-key" not in result.consumer_ref


def test_resolver_captures_request_metadata():
    resolver = HttpAttributionResolver()

    request = make_request(
        headers={"User-Agent": "pytest-client"},
        path="/candles/hyperliquid/futures/ETH-USDC/1m",
        method="GET",
    )

    result = resolver.resolve(request)

    assert result.path == "/candles/hyperliquid/futures/ETH-USDC/1m"
    assert result.method == "GET"
    assert result.user_agent == "pytest-client"
    assert result.received_at is not None

def test_resolver_ignores_empty_x_forwarded_for_and_uses_client_host():
    resolver = HttpAttributionResolver()

    request = make_request(
        headers={"X-Forwarded-For": "   "},
        host="127.0.0.1",
    )

    result = resolver.resolve(request)

    assert result.source_ip == "127.0.0.1"
    assert result.ip_source == "direct"

def test_resolver_treats_empty_api_key_as_public_consumer():
    resolver = HttpAttributionResolver()

    request = make_request(
        headers={"X-API-Key": ""},
        host="127.0.0.1",
    )

    result = resolver.resolve(request)

    assert result.consumer_type == "public"
    assert result.consumer_ref == "ip:127.0.0.1"
    assert result.api_key_fingerprint is None

    