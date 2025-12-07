from dataclasses import dataclass
from core.models.enums import Exchange, MarketType, interval

@dataclass(frozen=True)
class Candle:
    timstapmp: int

    open: float
    high: float
    low: float
    close: float
    volume: float

    exchange: Exchange
    market_type: MarketType
    symbol: str
    interval: interval

