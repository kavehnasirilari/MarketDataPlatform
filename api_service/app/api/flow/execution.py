#api_service/app/api/flow/execution.py

import logging
import time
from api_service.app.attribution.base import AttributionResolver
from api_service.app.policy.base import PolicyEngine, PolicyDecisionType
from api_service.app.dataAccess.base import DataAccessor, MetadataAccessor
from api_service.app.semantics.base import SemanticAnnotator
from api_service.app.api.flow.consumption.snapshot import ConsumptionState


logger = logging.getLogger(__name__)

class ExecutionOrchestrator:
    """مدیریت جریان اجرای درخواست از ورودی تا خروجی"""

    def __init__(
        self,
        attribution: AttributionResolver,
        policy: PolicyEngine,
        data: DataAccessor,
        metadata: MetadataAccessor,
        semantics: SemanticAnnotator,
    ):
        self.attribution = attribution
        self.policy = policy
        self.data = data
        self.metadata = metadata
        self.semantics = semantics
        self.consumption_state = ConsumptionState(window_seconds=60)

    def handle_request(self, request, route: str, payload: dict):

        start = time.perf_counter()

        logger.info("Execution started", extra={"path": request.url.path})


        attribution_ctx = self.attribution.resolve(request)

        logger.info(
            "Attribution resolved", 
            extra={
                "event": "Attribution resolved",
                "request_id": attribution_ctx.request_id,
                "consumer_ref": attribution_ctx.consumer_ref,
                "consumer_type": attribution_ctx.consumer_type,
                "source_ip": attribution_ctx.source_ip,
                "ip_source": attribution_ctx.ip_source,
                "path": attribution_ctx.path,
                "method": attribution_ctx.method,
            },
        )
        
        snapshot = self.consumption_state.observe_and_update(
            consumer_ref=attribution_ctx.consumer_ref,
            units=1,
        )


        policy_decision = self.policy.evaluate(snapshot, attribution_ctx, request)
        logger.info(
            "Policy evaluated", 
            extra={
                "event": "Policy evaluated", 
                "request_id": attribution_ctx.request_id,
                "consumer_ref": attribution_ctx.consumer_ref,
                "decision": policy_decision.decision.name,
            },
        )


        if policy_decision.decision != PolicyDecisionType.ALLOW:
            semantic = self.semantics.annotate(
                policy_decision=policy_decision
            )
            logger.info(
                "Execution completed (policy rejection)",
                extra={
                    "event": "Execution completed (policy rejection)",
                    "request_id": attribution_ctx.request_id,
                    "consumer_ref": attribution_ctx.consumer_ref,
                },
            )

            logger.info(
                "Summery (policy rejection)",
                extra={
                    "consumer_type":attribution_ctx.consumer_type,
                    "path":attribution_ctx.source_ip,
                    "policy_decision":policy_decision.decision.name,
                    "semantic_type" :semantic.type,
                    "semantic_msg" :semantic.message
                }
            )   

            return semantic

        if route == 'gat_candle':
            data_result = self.data.fetch(request, payload)
        elif route == 'get_metadata':
            data_result = self.metadata.fetch(request, payload)
        logger.info(
            "Data fetched",
            extra={
                "event": "Data fetched",
                "request_id": attribution_ctx.request_id,
                "consumer_ref": attribution_ctx.consumer_ref,
                "available": data_result.available,
            },
        )
        

        semantic_response = self.semantics.annotate(policy_decision = policy_decision ,data_result= data_result)
        logger.info(
            "Semantics applied",
            extra={
                "event": "Semantics applied",
                "request_id": attribution_ctx.request_id,
                "consumer_ref": attribution_ctx.consumer_ref,
            },
        )

        logger.info(
            "Execution completed",
            extra={
                "event": "Execution completed",
                "request_id": attribution_ctx.request_id,
                "consumer_ref": attribution_ctx.consumer_ref,
            },
        )

        latency_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "Summery",
            extra={
                "consumer_type":attribution_ctx.consumer_type,
                "path":attribution_ctx.source_ip,
                "policy_decision":policy_decision.decision.name,
                "data_available":data_result.available,
                "semantic_type" :semantic_response.type,
                "semantic_msg" :semantic_response.message,
                "latency": latency_ms
            }
        )        
        return semantic_response
