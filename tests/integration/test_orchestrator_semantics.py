from types import SimpleNamespace

from api_service.app.api.flow.execution import ExecutionOrchestrator
from api_service.app.policy.base import PolicyDecision, PolicyDecisionType
from api_service.app.dataAccess.base import DataResault
from api_service.app.semantics.mock_impl import MockSemanticAnnotator


class FakeAttributionResolver:
    def resolve(self, request):
        return SimpleNamespace(
            request_id="test-request-id",
            consumer_ref="ip:testclient",
            consumer_type="public",
            source_ip="testclient",
            ip_source="direct",
            path=request.url.path,
            method=request.method,
        )


class AllowPolicyEngine:
    def evaluate(self, snapshot, attribution_ctx, request):
        return PolicyDecision(
            decision=PolicyDecisionType.ALLOW,
            reason="allowed",
        )


class DenyPolicyEngine:
    def evaluate(self, snapshot, attribution_ctx, request):
        return PolicyDecision(
            decision=PolicyDecisionType.DENY,
            reason="denied by test policy",
        )


class AvailableDataAccessor:
    def fetch(self, request, payload):
        return DataResault(
            available=True,
            message="success",
            payload=[
                {
                    "timestamp": 1,
                    "open": 1,
                    "high": 2,
                    "low": 1,
                    "close": 2,
                    "volume": 10,
                }
            ],
        )


class UnavailableDataAccessor:
    def fetch(self, request, payload):
        return DataResault(
            available=False,
            payload=None,
            message="not found",
        )


class FakeMetadataAccessor:
    def fetch(self, request, payload):
        return DataResault(
            available=True,
            payload={"exchanges": []},
        )


def fake_request():
    return SimpleNamespace(
        method="GET",
        url=SimpleNamespace(path="/test"),
        client=SimpleNamespace(host="testclient"),
        headers={},
    )


def test_orchestrator_returns_success_when_data_is_available():
    orchestrator = ExecutionOrchestrator(
        attribution=FakeAttributionResolver(),
        policy=AllowPolicyEngine(),
        data=AvailableDataAccessor(),
        metadata=FakeMetadataAccessor(),
        semantics=MockSemanticAnnotator(),
    )

    result = orchestrator.handle_request(
        request=fake_request(),
        route="get_candles",
        payload={},
    )

    assert result.type == "success"
    assert result.message is None
    assert isinstance(result.data, list)
    assert len(result.data) > 0


def test_orchestrator_returns_error_when_data_is_unavailable():
    orchestrator = ExecutionOrchestrator(
        attribution=FakeAttributionResolver(),
        policy=AllowPolicyEngine(),
        data=UnavailableDataAccessor(),
        metadata=FakeMetadataAccessor(),
        semantics=MockSemanticAnnotator(),
    )

    result = orchestrator.handle_request(
        request=fake_request(),
        route="get_candles",
        payload={},
    )

    assert result.type == "error"
    assert result.message == "not found"
    assert result.data is None


def test_orchestrator_returns_error_when_policy_denies_request():
    orchestrator = ExecutionOrchestrator(
        attribution=FakeAttributionResolver(),
        policy=DenyPolicyEngine(),
        data=AvailableDataAccessor(),
        metadata=FakeMetadataAccessor(),
        semantics=MockSemanticAnnotator(),
    )

    result = orchestrator.handle_request(
        request=fake_request(),
        route="get_candles",
        payload={},
    )

    assert result.type == "error"
    assert result.message == "denied by test policy"
    assert result.data is None


def test_orchestrator_routes_candle_requests_to_data_accessor():
    class TrackingDataAccessor:
        def __init__(self):
            self.called = False

        def fetch(self, request, payload):
            self.called = True
            return DataResault(
                available=True,
                message="success",
                payload=[{"source": "data"}],
            )

    class TrackingMetadataAccessor:
        def __init__(self):
            self.called = False

        def fetch(self, request, payload):
            self.called = True
            return DataResault(
                available=True,
                message="success",
                payload={"source": "metadata"},
            )

    data = TrackingDataAccessor()
    metadata = TrackingMetadataAccessor()

    orchestrator = ExecutionOrchestrator(
        attribution=FakeAttributionResolver(),
        policy=AllowPolicyEngine(),
        data=data,
        metadata=metadata,
        semantics=MockSemanticAnnotator(),
    )

    result = orchestrator.handle_request(
        request=fake_request(),
        route="get_candles",
        payload={},
    )

    assert data.called is True
    assert metadata.called is False
    assert result.data == [{"source": "data"}]


def test_orchestrator_routes_metadata_requests_to_metadata_accessor():
    class TrackingDataAccessor:
        def __init__(self):
            self.called = False

        def fetch(self, request, payload):
            self.called = True
            return DataResault(
                available=True,
                message="success",
                payload=[{"source": "data"}],
            )

    class TrackingMetadataAccessor:
        def __init__(self):
            self.called = False

        def fetch(self, request, payload):
            self.called = True
            return DataResault(
                available=True,
                message="success",
                payload={"source": "metadata"},
            )

    data = TrackingDataAccessor()
    metadata = TrackingMetadataAccessor()

    orchestrator = ExecutionOrchestrator(
        attribution=FakeAttributionResolver(),
        policy=AllowPolicyEngine(),
        data=data,
        metadata=metadata,
        semantics=MockSemanticAnnotator(),
    )

    result = orchestrator.handle_request(
        request=fake_request(),
        route="get_metadata",
        payload={},
    )

    assert data.called is False
    assert metadata.called is True
    assert result.data == {"source": "metadata"}


    
