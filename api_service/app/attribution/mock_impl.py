# domain/attribution/mock_impl.py
from .base import AttributionResolver, AttributionContext
import uuid

class MockAttributionResolver(AttributionResolver):
    def resolve(self, request) -> AttributionContext:
        return AttributionContext(
            request_id=str(uuid.uuid4()),
            consumer_tier="public",
            source_ip=request.client.host
        )
