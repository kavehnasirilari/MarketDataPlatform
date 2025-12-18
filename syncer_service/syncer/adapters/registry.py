# syncer_service\syncer\adapters\registry.py
"""
Adapter registry for Phase 4A.1 (Exchange-level sync)

Design decision:
- Phase 4A.1 only operates at EXCHANGE level.
- We do NOT instantiate adapters here.
- We do NOT perform network calls.
- We do NOT deal with market / symbol / interval yet.

This registry MUST exactly reflect existing adapter implementations.
If an adapter does not exist in core.adapters, it must NOT appear here.
"""

from core.adapters.binance import BinanceAdapter
from core.adapters.hyperliquid import HyperliquidAdapter

# IMPORTANT:
# Coinbase adapter is NOT implemented yet,
# therefore it is intentionally NOT included here.

ADAPTER_REGISTRY = {
    "binance": BinanceAdapter,
    "hyperliquid": HyperliquidAdapter,
}
