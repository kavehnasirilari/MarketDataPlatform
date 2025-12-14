from core.models.enums import Exchange, Interval
from core.exceptions import MappingError

INTERVAL_MAPPING: dict[Exchange, dict[Interval, str]] = {
    Exchange.BINANCE: {
        Interval.M1: "1m",
        Interval.M5: "5m",
        Interval.M15: "15m",
        Interval.H1: "1h",
    },
    Exchange.HYPERLIQUID: {
        Interval.M1: "1m",
        Interval.M5: "5m",
        Interval.M15: "15m",
        Interval.H1: "1h",
    },
}


def map_interval(exchange: Exchange, interval: Interval) -> str:
    """Map canonical Interval to exchange-specific interval string."""
    try:
        return INTERVAL_MAPPING[exchange][interval]
    except KeyError as exc:
        raise MappingError(
            f"Interval mapping not found for exchange={exchange.value}, interval={interval.value}"
        ) from exc