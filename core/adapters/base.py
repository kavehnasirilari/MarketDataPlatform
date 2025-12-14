#core\adapters\base.py

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List

from core.mapping.interval_mapping import map_interval
from core.mapping.symbol_mapping import map_symbol

from core.models.candle import Candle
from core.models.enums import Exchange, MarketType, Interval
from core.exceptions import (
    AdapterError,
    MappingError,
    CandleValidationError,
)

class BaseAdapter(ABC):
    """Abstract base class for exchange adapters.
    Each concrete adapter must define:
        - self.exchange
        - self.market_type
    and implement the required abstract methods."""
    exchange: Exchange
    market_type: MarketType


    #-----------------------------
    # public high level api
    #-----------------------------
    def fetch_candles(
        self,
        symbol: str,
        interval: Interval,
        limit: int = 500,
    ) -> List[Candle]:
        """
        Standard candle-fetching pipeline for all adapters.

        Steps:
        1) normalize symbol & interval
        2) fetch raw data from exchange
        3) validate raw response
        4) convert each raw item into a canonical Candle
        """
        try:          
            # step 1: symbol & interval mapping
            exchange_symbol = self.normalize_symbol(symbol)
            exchange_interval = self.normalize_interval(interval)
            
            # step 2: call exchange api
            raw_items = self.fetch_raw_candles(
                exchange_symbol,
                exchange_interval,
                limit,
            )

            # step 3: validate raw response
            self.validate_response(raw_items)

            # step 4: map raw items to canonical Candle
            candles: List[Candle] = []
            for item in raw_items:
                candle = self.to_candle(
                    raw_item = item,
                    symbol = symbol,
                    interval = interval,
                    )
                self._validate_candle(candle)
                candles.append(candle)
            return candles

        except MappingError:
            raise
        except CandleValidationError:
            raise
        except Exception as e:
            raise AdapterError(
                f"Error fetching candles from {self.exchange.value} "
                f"for {symbol} at {interval.value}: {str(e)}"
            ) from e
            
    @abstractmethod
    def fetch_raw_candles(
        self,
        exchange_symbol: str,
        exchange_interval: str,
        limit: int,
    ) -> list[Any]:
        """ 
        fetch raw candles directly from exchange api.
        
        this mthod must:
        - call the exchange api
        - return raw response itmes (whith no normalization or mapping)
        """
        raise NotImplementedError
    #-----------------------------

    def normalize_symbol(self, symbol: str) -> str:
        """
        convert canonical symbol (e.g. 'btc)
        to the exchange-spesiic symbol format
        
        this method must raise MappingError when mapping is not possible
        """
        return map_symbol(self.exchange, symbol)
    #-----------------------------

    def normalize_interval(self, interval: Interval) -> str:
        """
        Convert a cannonical interval to the exchange-spesific interval representation.
        
        Must raise Mapping Error if mapping is not possible.
        """
        return map_interval(self.exchange, interval)
    #-----------------------------

    @abstractmethod
    def to_candle(
        self,
        raw_item: Any,
        symbol: str,
        interval: Interval,
    ) -> Candle:
        """
        Convert a raw exchange response to canonical candle format.
        """
        raise NotImplementedError
    #-----------------------------

    def validate_response(self, raw_items: list[Any]) -> None:
        """
        validate the raw itmes received from exchange api.
        
        Default behavior:
        - raw items must be a list
        - empty list is allowed
        """
        if not isinstance(raw_items, list):
            raise AdapterError(
                f"Expected list of raw candle items, got {type(raw_items)}"
            )
        
    def _validate_candle(self, candle: Candle) -> None:
        """
        internal method to validate constructed candle object.
        enforce core invariants.
        """


        # timestamps
        if candle.open_timestamp <= 0:
            raise CandleValidationError("Open timestamp must be positive")
        
        if candle.close_timestamp <= candle.open_timestamp:
            raise CandleValidationError("close timestamp must be after open timestamp")
        
        # prices integrity
        if (candle.open is None
        or candle.high is None
        or candle.low is None
        or candle.close is None
        ):
            raise CandleValidationError("Candle prices must not be None")
        
        if candle.high < max(candle.open, candle.close):
            raise CandleValidationError("Candle high price is less than open/close price")

        if candle.low > min(candle.open, candle.close):
            raise CandleValidationError("Candle low price is greater than open/close price")
        
        # volume
        if candle.volume is None or candle.volume < 0:
            raise CandleValidationError("Candle volume must be non-negative")
        
        # metadata consistency
        if candle.exchange != self.exchange:
            raise CandleValidationError("Candle exchange does not match adapter exchange")
        
        if candle.market_type != self.market_type:
            raise CandleValidationError("Candle market type does not match adapter market type")
        

