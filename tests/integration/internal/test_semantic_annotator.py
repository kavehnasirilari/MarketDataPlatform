from dataclasses import dataclass

from api_service.app.policy.base import PolicyDecision, PolicyDecisionType
from api_service.app.semantics.mock_impl import MockSemanticAnnotator


@dataclass
class FakeDataResult:
    available: bool
    message: str
    payload: object


def test_semantic_annotator_returns_success_when_policy_allowed_and_data_available():
    annotator = MockSemanticAnnotator()

    policy_decision = PolicyDecision(
        decision=PolicyDecisionType.ALLOW,
        reason="allowed",
    )

    data_result = FakeDataResult(
        available=True,
        message="ok",
        payload=[{"symbol": "BTC-USDT"}],
    )

    result = annotator.annotate(
        policy_decision=policy_decision,
        data_result=data_result,
    )

    assert result.type == "success"
    assert result.message is None
    assert result.data == [{"symbol": "BTC-USDT"}]


def test_semantic_annotator_returns_error_when_policy_denied():
    annotator = MockSemanticAnnotator()

    policy_decision = PolicyDecision(
        decision=PolicyDecisionType.DENY,
        reason="rate limit exceeded",
    )

    data_result = FakeDataResult(
        available=True,
        message="ok",
        payload=[{"symbol": "BTC-USDT"}],
    )

    result = annotator.annotate(
        policy_decision=policy_decision,
        data_result=data_result,
    )

    assert result.type == "error"
    assert result.message == "rate limit exceeded"
    assert result.data is None


def test_semantic_annotator_returns_error_when_data_not_available():
    annotator = MockSemanticAnnotator()

    policy_decision = PolicyDecision(
        decision=PolicyDecisionType.ALLOW,
        reason="allowed",
    )

    data_result = FakeDataResult(
        available=False,
        message="not find",
        payload=None,
    )

    result = annotator.annotate(
        policy_decision=policy_decision,
        data_result=data_result,
    )

    assert result.type == "error"
    assert result.message == "not find"
    assert result.data is None