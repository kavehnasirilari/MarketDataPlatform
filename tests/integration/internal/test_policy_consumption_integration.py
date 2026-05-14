from api_service.app.api.flow.consumption.snapshot import ConsumptionState
from api_service.app.policy.base import PolicyDecisionType
from api_service.app.policy.mock_impl import MockPolicyEngine


def test_policy_allows_consumption_under_limit(monkeypatch):
    monkeypatch.setattr(
        "api_service.app.api.flow.consumption.snapshot.time.time",
        lambda: 1000.0,
    )

    state = ConsumptionState(window_seconds=60)
    policy = MockPolicyEngine()

    snapshot = state.observe_and_update(
        consumer_ref="ip:127.0.0.1",
        units=1,
    )

    decision = policy.evaluate(
        snapshot=snapshot,
        attribution_ctx=None,
        request=None,
    )

    assert decision.decision == PolicyDecisionType.ALLOW


def test_policy_denies_consumption_over_limit(monkeypatch):
    monkeypatch.setattr(
        "api_service.app.api.flow.consumption.snapshot.time.time",
        lambda: 1000.0,
    )

    state = ConsumptionState(window_seconds=60)
    policy = MockPolicyEngine()

    snapshot = state.observe_and_update(
        consumer_ref="ip:127.0.0.1",
        units=301,
    )

    decision = policy.evaluate(
        snapshot=snapshot,
        attribution_ctx=None,
        request=None,
    )

    assert decision.decision == PolicyDecisionType.DENY
    assert decision.reason == "rate limit exceeded for consumer_ref=ip:127.0.0.1"




