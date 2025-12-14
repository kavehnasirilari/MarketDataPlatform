from dataclasses import dataclass
from core.models.enums import Exchange, MarketType, Interval

@dataclass(frozen=True)
class Candle:
    open_timestamp: int
    close_timestamp: int

    open: float
    high: float
    low: float
    close: float
    volume: float

    exchange: Exchange
    market_type: MarketType
    symbol: str
    interval: Interval

