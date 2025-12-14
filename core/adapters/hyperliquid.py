from core.adapters.base import BaseAdapter
from typing import List, Any
from core.models.enums import MarketType, Exchange, Interval
from core.models.candle import Candle
import requests
import time

class HyperliquidAdapter(BaseAdapter):

    exchange = Exchange.HYPERLIQUID

    INTERVAL_MS = {
    "1m": 60_000,
    "3m": 3 * 60_000,
    "5m": 5 * 60_000,
    "15m": 15 * 60_000,
    "30m": 30 * 60_000,
    "1h": 60 * 60_000,
    "2h": 2 * 60 * 60_000,
    "4h": 4 * 60 * 60_000,
    "8h": 8 * 60 * 60_000,
    "12h": 12 * 60 * 60_000,
    "1d": 24 * 60 * 60_000,
    "3d": 3 * 24 * 60 * 60_000,
    "1w": 7 * 24 * 60 * 60_000,
    }

    def __init__(self, market_type: MarketType):
        self.market_type = market_type


    def fetch_raw_candles(
            self, 
            exchange_symbol: str, 
            exchange_interval: str, 
            limit: int
            ) -> List[Any]:
        
        end_time = int(time.time() * 1000)
        interval_ms = self.INTERVAL_MS[exchange_interval]
        start_time = end_time - (interval_ms * limit)


        endpoint = self._get_klines_endpoint()

        payload = {
        "type": "candleSnapshot",
        "req": {
            "coin": exchange_symbol,
            "interval": exchange_interval,
            "startTime": start_time,
            "endTime": end_time,
            },
        }

        response = requests.post(
            endpoint, 
            json=payload, 
            timeout=10)
        response.raise_for_status()
        return response.json()

    def to_candle(
            self, 
            raw_item : dict[str, Any], 
            symbol : str, 
            interval : Interval
        ) -> Candle:

        return Candle(
            open_timestamp=int(raw_item["t"]),
            close_timestamp=int(raw_item["T"]),
            open=float(raw_item["o"]),
            high=float(raw_item["h"]),
            low=float(raw_item["l"]),
            close=float(raw_item["c"]),
            volume=float(raw_item["v"]),
            exchange=self.exchange,
            market_type=self.market_type,
            symbol=symbol,
            interval=interval,
        )


    def _get_klines_endpoint(self) -> str:

        if self.market_type != MarketType.FUTURES:
            raise ValueError(f"Unsupported market type: {self.market_type}")
        
        return "https://api.hyperliquid.xyz/info"


