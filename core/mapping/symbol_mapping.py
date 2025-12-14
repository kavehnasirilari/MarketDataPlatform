from core.models.enums import Exchange
from core.exceptions import MappingError

SYMBOL_MAPPING: dict[Exchange, dict[str, str]] = {
    Exchange.BINANCE: {
        "BTC/USDT": "BTCUSDT",
        "ETH/USDT": "ETHUSDT",
    },
    Exchange.HYPERLIQUID: {
        "BTC/USDC": "BTC",
        "ETH/USDC": "ETH",
    }
}

def map_symbol(exchange: Exchange, symbol: str) -> str:
    """ Map canonical symbol to exchange-specific symbol string."""
    try:
        return SYMBOL_MAPPING[exchange][symbol]
    except KeyError as exc:
        raise MappingError(
            f"Symbol mapping not found for exchange={exchange.value}, symbol={symbol}"
        ) from exc
