#core/exceptions.py

class CoreError(Exception):
    """Base class for all core exceptions."""
    pass

class AdapterError(CoreError):
    """Exception raised for errors related to adaptors."""
    pass

class MappingError(CoreError):
    """Exception raised for errors in mapping operations."""
    pass

class CandleValidationError(CoreError):
    """Exception raised for errors in candle data validation."""
    pass

class ExchangeNotSupportedError(CoreError):
    """Exception raised when an unsupported exchange is referenced."""
    pass



