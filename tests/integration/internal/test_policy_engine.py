from dataclasses import dataclass

from api_service.app.policy.base import PolicyDecisionType
from api_service.app.policy.mock_impl import MockPolicyEngine


@dataclass
class FakeConsumptionSnapshot:
    consumed_units: int
    consumer_ref: str = "ip:127.0.0.1"


def test_policy_engine_allows_when_consumed_units_is_not_over_limit():
    engine = MockPolicyEngine()

    snapshot = FakeConsumptionSnapshot(consumed_units=3)

    result = engine.evaluate(
        snapshot=snapshot,
        attribution_ctx=None,
        request=None,
    )

    assert result.decision == PolicyDecisionType.ALLOW
    assert result.reason == "noosh jan"


def test_policy_engine_denies_when_consumed_units_is_over_limit():
    engine = MockPolicyEngine()

    snapshot = FakeConsumptionSnapshot(
        consumed_units=301,
        consumer_ref="ip:127.0.0.1",
    )

    result = engine.evaluate(
        snapshot=snapshot,
        attribution_ctx=None,
        request=None,
    )

    assert result.decision == PolicyDecisionType.DENY
    assert result.reason == "rate limit exceeded for consumer_ref=ip:127.0.0.1"