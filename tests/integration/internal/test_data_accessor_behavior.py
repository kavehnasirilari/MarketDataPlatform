from api_service.app.dataAccess.mock_impl import MockDataAccessor, MockMetaDataAccessor


class FakeResult:
    def __init__(self, rows):
        self.rows = rows

    def mappings(self):
        return self

    def all(self):
        return self.rows


class FakeSession:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def execute(self, query, params=None):
        self.calls.append((str(query), params or {}))
        return FakeResult(self.responses.pop(0))


class FakeSessionContext:
    def __init__(self, session):
        self.session = session

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc, tb):
        return False


def test_data_accessor_returns_not_available_when_exchange_not_found(monkeypatch):
    session = FakeSession(responses=[
        [],  # exchanges
    ])

    monkeypatch.setattr(
        "api_service.app.dataAccess.mock_impl.get_session",
        lambda: FakeSessionContext(session),
    )

    accessor = MockDataAccessor()

    result = accessor.fetch(
        request=None,
        payload={
            "exchange": "unknown",
            "symbol": "BTC-USDT",
            "market": "spot",
            "interval": "1m",
        },
    )

    assert result.available is False
    assert result.message == "exchange not find"
    assert result.payload == []


def test_data_accessor_normalizes_symbol_dash_to_slash(monkeypatch):
    session = FakeSession(responses=[
        [{"id": 1, "name": "binance"}],          # exchanges
        [{"id": 10, "symbol": "BTC/USDT"}],     # canonical_symbols
        [],                                     # exchange_markets
    ])

    monkeypatch.setattr(
        "api_service.app.dataAccess.mock_impl.get_session",
        lambda: FakeSessionContext(session),
    )

    accessor = MockDataAccessor()

    accessor.fetch(
        request=None,
        payload={
            "exchange": "binance",
            "symbol": "BTC-USDT",
            "market": "spot",
            "interval": "1m",
        },
    )

    symbol_query_params = session.calls[1][1]

    assert symbol_query_params == {"symbol": "BTC/USDT"}


def test_data_accessor_returns_available_when_candles_exist(monkeypatch):
    candle_rows = [
        {"open_time": 1000, "open": 1, "high": 2, "low": 1, "close": 2},
    ]

    session = FakeSession(responses=[
        [{"id": 1, "name": "binance"}],         # exchanges
        [{"id": 10, "symbol": "BTC/USDT"}],    # canonical_symbols
        [{"id": 100}],                         # exchange_markets
        [{"id": 5, "interval": "1m"}],         # intervals
        candle_rows,                           # candles
    ])

    monkeypatch.setattr(
        "api_service.app.dataAccess.mock_impl.get_session",
        lambda: FakeSessionContext(session),
    )

    accessor = MockDataAccessor()

    result = accessor.fetch(
        request=None,
        payload={
            "exchange": "binance",
            "symbol": "BTC-USDT",
            "market": "spot",
            "interval": "1m",
        },
    )

    assert result.available is True
    assert result.message == "success"
    assert result.payload == candle_rows


def test_metadata_accessor_groups_rows_into_tree_response(monkeypatch):
    rows = [
        {
            "exchange": "binance",
            "symbol": "BTC-USDT",
            "exchange_symbol": "BTCUSDT",
            "interval": "1m",
            "market_type": "spot",
            "status": "active",
        },
        {
            "exchange": "binance",
            "symbol": "BTC-USDT",
            "exchange_symbol": "BTCUSDT",
            "interval": "5m",
            "market_type": "spot",
            "status": "active",
        },
    ]

    session = FakeSession(responses=[rows])

    monkeypatch.setattr(
        "api_service.app.dataAccess.mock_impl.get_session",
        lambda: FakeSessionContext(session),
    )

    accessor = MockMetaDataAccessor()

    result = accessor.fetch(
        request=None,
        payload={"exchange": "binance", "market": "spot"},
    )

    assert result.available is True
    assert result.payload == {
        "exchanges": [
            {
                "name": "binance",
                "markets": [
                    {
                        "symbol": "BTC-USDT",
                        "exchange_symbol": "BTCUSDT",
                        "market_type": "spot",
                        "intervals": ["1m", "5m"],
                    }
                ],
            }
        ]
    }


def test_metadata_accessor_returns_empty_tree_when_no_rows(monkeypatch):
    session = FakeSession(responses=[[]])

    monkeypatch.setattr(
        "api_service.app.dataAccess.mock_impl.get_session",
        lambda: FakeSessionContext(session),
    )

    accessor = MockMetaDataAccessor()

    result = accessor.fetch(
        request=None,
        payload={"exchange": "unknown"},
    )

    assert result.available is False
    assert result.payload == {"exchanges": []}


def test_data_accessor_returns_not_available_when_exchange_market_not_found(monkeypatch):
    session = FakeSession(responses=[
        [{"id": 1, "name": "binance"}],       # exchanges
        [{"id": 10, "symbol": "BTC/USDT"}],  # canonical_symbols
        [],                                  # exchange_markets
    ])

    monkeypatch.setattr(
        "api_service.app.dataAccess.mock_impl.get_session",
        lambda: FakeSessionContext(session),
    )

    accessor = MockDataAccessor()

    result = accessor.fetch(
        request=None,
        payload={
            "exchange": "binance",
            "symbol": "BTC-USDT",
            "market": "spot",
            "interval": "1m",
        },
    )

    assert result.available is False
    assert result.message == "exchange_market not find"
    assert result.payload == []


def test_data_accessor_returns_not_available_when_interval_not_found(monkeypatch):
    session = FakeSession(responses=[
        [{"id": 1, "name": "binance"}],       # exchanges
        [{"id": 10, "symbol": "BTC/USDT"}],  # canonical_symbols
        [{"id": 100}],                       # exchange_markets
        [],                                  # intervals
    ])

    monkeypatch.setattr(
        "api_service.app.dataAccess.mock_impl.get_session",
        lambda: FakeSessionContext(session),
    )

    accessor = MockDataAccessor()

    result = accessor.fetch(
        request=None,
        payload={
            "exchange": "binance",
            "symbol": "BTC-USDT",
            "market": "spot",
            "interval": "999m",
        },
    )

    assert result.available is False
    assert result.message == "Interval not find"
    assert result.payload == []    


def test_metadata_accessor_applies_all_supported_filters(monkeypatch):
    session = FakeSession(responses=[[]])

    monkeypatch.setattr(
        "api_service.app.dataAccess.mock_impl.get_session",
        lambda: FakeSessionContext(session),
    )

    accessor = MockMetaDataAccessor()

    accessor.fetch(
        request=None,
        payload={
            "exchange": "binance",
            "market": "futures",
            "symbol": "BTC-USDT",
            "interval": "1m",
        },
    )

    query, params = session.calls[0]

    assert "e.name = :exchange" in query
    assert "em.market_type = :market" in query
    assert "REPLACE(cs.symbol, '/', '-') = :symbol" in query
    assert "i.interval = :interval" in query

    assert params == {
        "exchange": "binance",
        "market": "futures",
        "symbol": "BTC-USDT",
        "interval": "1m",
    }


def test_metadata_accessor_groups_multiple_exchanges_and_markets(monkeypatch):
    rows = [
        {
            "exchange": "binance",
            "symbol": "BTC-USDT",
            "exchange_symbol": "BTCUSDT",
            "interval": "1m",
            "market_type": "spot",
            "status": "active",
        },
        {
            "exchange": "binance",
            "symbol": "ETH-USDT",
            "exchange_symbol": "ETHUSDT",
            "interval": "1m",
            "market_type": "futures",
            "status": "active",
        },
        {
            "exchange": "hyperliquid",
            "symbol": "BTC-USDC",
            "exchange_symbol": "BTC",
            "interval": "5m",
            "market_type": "futures",
            "status": "active",
        },
    ]

    session = FakeSession(responses=[rows])

    monkeypatch.setattr(
        "api_service.app.dataAccess.mock_impl.get_session",
        lambda: FakeSessionContext(session),
    )

    result = MockMetaDataAccessor().fetch(request=None, payload={})

    assert result.available is True
    assert len(result.payload["exchanges"]) == 2
    

def test_metadata_accessor_deduplicates_duplicate_intervals(monkeypatch):
    rows = [
        {
            "exchange": "binance",
            "symbol": "BTC-USDT",
            "exchange_symbol": "BTCUSDT",
            "interval": "1m",
            "market_type": "spot",
            "status": "active",
        },
        {
            "exchange": "binance",
            "symbol": "BTC-USDT",
            "exchange_symbol": "BTCUSDT",
            "interval": "1m",
            "market_type": "spot",
            "status": "active",
        },
    ]

    session = FakeSession(responses=[rows])

    monkeypatch.setattr(
        "api_service.app.dataAccess.mock_impl.get_session",
        lambda: FakeSessionContext(session),
    )

    result = MockMetaDataAccessor().fetch(
        request=None,
        payload={},
    )

    intervals = result.payload["exchanges"][0]["markets"][0]["intervals"]

    assert intervals == ["1m"]



