# api_service/app/cache/metedata_cache.py

import hashlib
import json
from typing import Any
import logging

logger = logging.getLogger(__name__)

from core.redis_client import build_redis_client

METADATA_CACHE_TTL_SECONDS = 300
METADATA_CACHE_VERSION  = "v1"

def build_metadata_cache_key(payload: dict[str, Any]) -> str:
    
    #  ساخت یک دیکشنری از صرافی و مارکت و سمبول و اینتروال های موجود در پیلود و مقدارشون
    # {صرافی: فلان، مارکت: بیسار، سمبول: ایکس، اینتروال: یک دقیقه}
    # این یک ابجکت پایتونی است
    normalized_payload = {
        key: payload.get(key)
        for key in ["exchange", "market", "symbol", "interval"]
        if payload.get(key)
    }

    # تبدیل ابجکت پایتونی به استرینگ با تابع جیسون دامپس
    # دستور سورت با پارامتر دوم
    # مشخص کردن سپریتور ها و در نهایت حذف فاصله ها
    raw = json.dumps(
        normalized_payload,
        sort_keys=True,
        separators=(",", ":")
    )

    # تبدیل خروجی بالا به کلید هش شده
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    
    return f"metadata:{METADATA_CACHE_VERSION}:{digest}"

def get_cached_metadata(payload: dict[str, Any]) -> dict[str, Any] | None:
    try:
        cache_key = build_metadata_cache_key(payload)
        client = build_redis_client()

        cached_value = client.get(cache_key)

        if cached_value is None:
            return None
        
        return json.loads(cached_value)
    except Exception:
        logger.exception(
            "Redis metadata cache read failed",
            extra={
                "service": "api-service",
                "event": "metadata.cache.read_failed",
                "status": "degraded",
                "operation": "cache_read",
            },
        )
        return None
    
def set_cached_metadata(payload: dict[str, Any], metadata: dict[str, Any]) -> None:
    try:
        cache_key = build_metadata_cache_key(payload)
        client = build_redis_client()

        client.set(
            cache_key,
            json.dumps(
                metadata, 
                sort_keys=True,
                separators=(",", ":")),
            ex=METADATA_CACHE_TTL_SECONDS,
        )
    except Exception:
        logger.exception(
            "Redis metadata cache write failed",
            extra={
                "service": "api-service",
                "event": "metadata.cache.write_failed",
                "status": "degraded",
                "operation": "cache_write",
            },
        )
        return None