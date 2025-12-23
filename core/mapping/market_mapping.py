
# core/mapping/market_mapping.py

from core.models.enums import Exchange, MarketType

EXCHANGE_MARKET_MAPPING: dict[Exchange, list[MarketType]] = {
    Exchange.BINANCE: [
        MarketType.SPOT,
        MarketType.FUTURES,
    ],
    Exchange.HYPERLIQUID: [
        MarketType.FUTURES,
    ],
}
