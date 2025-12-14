from enum import Enum

class Exchange(Enum):
    BINANCE = "binance"
    COINBASE = "coinbase"
    HYPERLIQUID = "hyperliquid"


class MarketType(Enum):
    SPOT = "spot"
    FUTURES = "futures"
    PREP = "prep"

class Interval(Enum):
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"
    W1 = "1w"
