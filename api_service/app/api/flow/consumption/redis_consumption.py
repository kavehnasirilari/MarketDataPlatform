# api_service/app/api/flow/consumption/redis_consumption.py

import logging
import time
import uuid

from api_service.app.api.flow.consumption.snapshot import ConsumptionSnapshot
from core.redis_client import build_redis_client

logger = logging.getLogger(__name__)


class RedisSlidingWindowConsumptionState:
    """
    Redis-backed Sliding Window consumption tracker.
    """
    def __init__(self, window_seconds: int):
        self.window_seconds = window_seconds
        self.redis = build_redis_client()

    def observe_and_update(
        self,
        consumer_ref: str,
        units: int = 1,
    ) -> ConsumptionSnapshot:

        now = time.time()
        window_start = now - self.window_seconds

        key = f"rate_limit:{consumer_ref}"


        try:
            pipe = self.redis.pipeline()

            pipe.zremrangebyscore(key, 0, window_start)

            for _ in range(units):
                member = str(uuid.uuid4())
                pipe.zadd(key, {member: now})

            pipe.zcard(key)
            pipe.expire(key, self.window_seconds)

            result = pipe.execute()

            consumed_units = result[-2]

            oldest_items = self.redis.zrange(key, 0, 0, withscores=True)

            if oldest_items:
                oldest_timestamp = oldest_items[0][1]
                remaining_window_seconds = int(
                    max(0, self.window_seconds - (now - oldest_timestamp))
                )
            else:
                remaining_window_seconds = self.window_seconds
            
            return ConsumptionSnapshot(
                consumer_ref=consumer_ref,
                consumed_units=consumed_units,
                remaining_window_seconds=remaining_window_seconds
            )
        
        except Exception:
            logger.exception(
                "Redis sliding-window rate limit unavailable",
                extra={
                    "service": "api-service",
                    "event": "rate_limit.redis_unavailable",
                    "status": "degraded",
                    "operation": "rate_limit",
                    "consumer_ref": consumer_ref,
                },
            )

            return ConsumptionSnapshot(
                consumer_ref=consumer_ref,
                consumed_units=1,
                remaining_window_seconds=self.window_seconds,
            )