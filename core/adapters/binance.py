from typing import List, Any
import requests
from core.adapters.base import BaseAdapter

from core.models.candle import Candle
from core.models.enums import Exchange, MarketType, Interval

class BinanceAdapter(BaseAdapter):
    
    exchange = Exchange.BINANCE

    def __init__(self, market_type: MarketType):
        self.market_type = market_type


    def fetch_raw_candles(
            self, 
            exchange_symbol: str, 
            exchange_interval: str, 
            limit: int
            ) -> List[Any]:
        """
        fetch raw candle data from Binance exchange API.
        implement depending on market type (spot, futures, etc.)
        """

        endpoint = self._get_klines_endpoint()
        params = {
            "symbol": exchange_symbol,
            "interval": exchange_interval,
            "limit": limit,
        }
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()

        return response.json()
        

    def to_candle(
            self, 
            raw_item: Any, 
            symbol: str, 
            interval: Interval
            ) -> Candle:
        """
        Make raw itme into canonical candle object.
        """
        return Candle(
            open_timestamp=int(raw_item[0]),
            close_timestamp=int(raw_item[6]),
            open=float(raw_item[1]),
            high=float(raw_item[2]),
            low=float(raw_item[3]),
            close=float(raw_item[4]),
            volume=float(raw_item[5]),
            exchange=self.exchange,
            market_type=self.market_type,
            symbol=symbol,
            interval=interval,
        )
    
    def _get_klines_endpoint(self) -> str:
        """
        Get the appropriate klines endpoint based on market type.
        """
        if self.market_type == MarketType.SPOT:
            return "https://api.binance.com/api/v3/klines"
        if self.market_type == MarketType.FUTURES:   
            return "https://fapi.binance.com/fapi/v1/klines"

        raise ValueError(f"Unsupported market type: {self.market_type}")    
    