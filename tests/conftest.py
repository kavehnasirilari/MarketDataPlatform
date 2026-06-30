import pytest

from core.redis_client import build_redis_client


@pytest.fixture(autouse=True)
def clean_redis_between_tests():
    redis_client = build_redis_client()
    redis_client.flushdb()

    yield

    redis_client.flushdb()