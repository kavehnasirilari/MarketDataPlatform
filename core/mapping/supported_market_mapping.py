# core/mapping/supported_market_mapping.py

from core.models.enums import Exchange, Interval, MarketType

SUPPORTED_MARKET_MAPPING = [
    # Binance BTC
    (Exchange.BINANCE, "BTC/USDT", Interval.M1, MarketType.SPOT),
    (Exchange.BINANCE, "BTC/USDT", Interval.M5, MarketType.SPOT),
    (Exchange.BINANCE, "BTC/USDT", Interval.M1, MarketType.FUTURES),
    (Exchange.BINANCE, "BTC/USDT", Interval.M5, MarketType.FUTURES),

    # Binance ETH
    (Exchange.BINANCE, "ETH/USDT", Interval.M1, MarketType.FUTURES),
    (Exchange.BINANCE, "ETH/USDT", Interval.M5, MarketType.FUTURES),

    # Hyperliquid (FUTURES)
    (Exchange.HYPERLIQUID, "BTC/USDC", Interval.M1, MarketType.FUTURES),
    (Exchange.HYPERLIQUID, "BTC/USDC", Interval.M5, MarketType.FUTURES),
]
