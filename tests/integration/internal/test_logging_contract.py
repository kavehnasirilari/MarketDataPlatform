import json
import logging
from types import SimpleNamespace

from api_service.app.api.flow.execution import ExecutionOrchestrator
from api_service.app.dataAccess.base import DataResault
from api_service.app.policy.base import PolicyDecision, PolicyDecisionType
from api_service.app.semantics.mock_impl import MockSemanticAnnotator

from core.observability.logging_config import JsonExtraFormatter


def test_json_extra_formatter_outputs_valid_json_with_base_fields():
    record = logging.LogRecord(
        name="test.logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    output = JsonExtraFormatter().format(record)
    data = json.loads(output)

    assert data["level"] == "INFO"
    assert data["logger"] == "test.logger"
    assert data["msg"] == "Test message"
    assert data["ts"].endswith("Z")


def test_json_extra_formatter_includes_extra_fields():
    record = logging.LogRecord(
        name="test.logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    record.request_id = "req-123"
    record.consumer_ref = "ip:testclient"

    output = JsonExtraFormatter().format(record)
    data = json.loads(output)

    assert data["request_id"] == "req-123"
    assert data["consumer_ref"] == "ip:testclient"


class FakeAttributionResolver:
    def resolve(self, request):
        return SimpleNamespace(
            request_id="req-123",
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


class AvailableDataAccessor:
    def fetch(self, request, payload):
        return DataResault(
            available=True,
            message="success",
            payload=[{"symbol": "BTC-USDT"}],
        )


class FakeMetadataAccessor:
    def fetch(self, request, payload):
        return DataResault(
            available=True,
            message="success",
            payload={"exchanges": []},
        )


def fake_request():
    return SimpleNamespace(
        method="GET",
        url=SimpleNamespace(path="/candles"),
        client=SimpleNamespace(host="testclient"),
        headers={},
    )


def test_execution_orchestrator_emits_expected_log_events(caplog):
    orchestrator = ExecutionOrchestrator(
        attribution=FakeAttributionResolver(),
        policy=AllowPolicyEngine(),
        data=AvailableDataAccessor(),
        metadata=FakeMetadataAccessor(),
        semantics=MockSemanticAnnotator(),
    )

    with caplog.at_level("INFO"):
        orchestrator.handle_request(
            request=fake_request(),
            route="get_candles",
            payload={},
        )

    events  = [getattr(record, "event", None) for record in caplog.records]

    assert "api.request.started" in events
    assert "api.request.attribution_resolved" in events
    assert "api.request.policy_evaluated" in events
    assert "api.request.data_fetched" in events
    assert "api.request.completed" in events


def test_summary_log_contains_expected_fields(caplog):
    orchestrator = ExecutionOrchestrator(
        attribution=FakeAttributionResolver(),
        policy=AllowPolicyEngine(),
        data=AvailableDataAccessor(),
        metadata=FakeMetadataAccessor(),
        semantics=MockSemanticAnnotator(),
    )

    with caplog.at_level("INFO"):
        orchestrator.handle_request(
            request=fake_request(),
            route="get_candles",
            payload={},
        )

    summary_record = next(
        record for record in caplog.records
        if getattr(record, "event", None) == "api.request.completed"
    )

    assert summary_record.consumer_type == "public"
    assert summary_record.policy_decision == "ALLOW"
    assert summary_record.data_available is True
    assert summary_record.semantic_type == "success"
    assert summary_record.latency_ms >= 0    