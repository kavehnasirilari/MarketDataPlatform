from database.session import get_session
from database.models import Exchange, CanonicalSymbol, Interval

def seed_initial_data():
    with get_session() as session:
        # Exchanges
        exchanges = [
            Exchange(name="binance"),
            Exchange(name="coinbase"),
            Exchange(name="hyperliquid"),
        ]
        session.add_all(exchanges)

        # Canonical Symbols
        symbols = [
            CanonicalSymbol(symbol="BTCUSDT", base_asset="BTC", quote_asset="USDT"),
            CanonicalSymbol(symbol="ETHUSDT", base_asset="ETH", quote_asset="USDT"),
        ]
        session.add_all(symbols)

        # Intervals
        intervals = [
            Interval(interval="1m", ms=60000),
            Interval(interval="15m", ms=900000),
            Interval(interval="1h", ms=3600000),
        ]
        session.add_all(intervals)

        session.commit()


if __name__ == "__main__":
    seed_initial_data()
