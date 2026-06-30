#  syncer_service/syncer/redis_lock.py

from __future__ import annotations

import uuid
from contextlib import contextmanager
from typing import Iterator

from core.redis_client import build_redis_client
from syncer_service.syncer.ingestion.types import IngestionUnit

SYNC_LOCK_TTL_SECONDS = 20

def build_candle_sync_lock_key(unit: IngestionUnit) -> str:
    return(
        "lock:syncer:candles:"
        f"{unit.exchange_name}:"
        f"{unit.market_type}:"
        f"{unit.canonical_symbol}:"
        f"{unit.interval}"

    )

@contextmanager
def candle_sync_lock(unit: IngestionUnit) -> Iterator[bool]:
    redis_client = build_redis_client()
    lock_key = build_candle_sync_lock_key(unit=unit)
    lock_token = str(uuid.uuid4())

    acquired = redis_client.set(
        lock_key,
        lock_token,
        nx=True,
        ex= SYNC_LOCK_TTL_SECONDS
    )

    if not acquired:
        yield False
        return
    
    try:
        yield True
    finally:
        current_token = redis_client.get(lock_key)

        if current_token == lock_token:
            redis_client.delete(lock_key)


