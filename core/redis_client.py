# core/redis_client.py

import os
from functools import lru_cache

import redis

@lru_cache(maxsize=1)
def build_redis_client() -> redis.Redis:
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        db=int(os.getenv("REDIS_DB", "0")),
        decode_responses=True,
    )