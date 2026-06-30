#api_service/app/api/flow/execution.py

import logging
import time
from api_service.app.attribution.base import AttributionResolver
from api_service.app.policy.base import PolicyEngine, PolicyDecisionType
from api_service.app.dataAccess.base import DataAccessor, MetadataAccessor
from api_service.app.semantics.base import SemanticAnnotator
from api_service.app.api.flow.consumption.redis_consumption import RedisSlidingWindowConsumptionState


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
        self.consumption_state = RedisSlidingWindowConsumptionState(window_seconds=60)

    def handle_request(self, request, route: str, payload: dict):

        start = time.perf_counter()
        attribution_ctx = None

        try:
            logger.info(
                "API request started",
                extra={
                    "service": "api-service",
                    "event": "api.request.started",
                    "status": "started",
                    "operation": route,
                    "path": request.url.path,
                    "method": request.method,
                },
            )

            attribution_ctx = self.attribution.resolve(request)

            logger.info(
                "Attribution resolved", 
                extra={
                    "service": "api-service",
                    "event": "api.request.attribution_resolved",
                    "status": "success",
                    "operation": route,
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
                    "service": "api-service",
                    "event": "api.request.policy_evaluated",
                    "status": "success",
                    "operation": route,
                    "request_id": attribution_ctx.request_id,
                    "consumer_ref": attribution_ctx.consumer_ref,
                    "policy_decision": policy_decision.decision.name,
                },
            )


            if policy_decision.decision != PolicyDecisionType.ALLOW:
                semantic = self.semantics.annotate(
                    policy_decision=policy_decision
                )
                latency_ms = (time.perf_counter() - start) * 1000
                
                logger.info(
                    "API request rejected by policy",
                    extra={
                        "service": "api-service",
                        "event": "api.request.policy_rejected",
                        "status": "rejected",
                        "operation": route,
                        "request_id": attribution_ctx.request_id,
                        "consumer_ref": attribution_ctx.consumer_ref,
                        "consumer_type": attribution_ctx.consumer_type,
                        "policy_decision": policy_decision.decision.name,
                        "semantic_type": semantic.type,
                        "semantic_msg": semantic.message,
                        "latency_ms": latency_ms,
                    },
                ) 

                return semantic

            if route == 'get_candles':
                data_result = self.data.fetch(request, payload)
            elif route == 'get_metadata':
                data_result = self.metadata.fetch(request, payload)
            else:
                raise ValueError(f"Unsupported API route: {route}")
            
            logger.info(
                "Data fetched",
                extra={
                    "service": "api-service",
                    "event": "api.request.data_fetched",
                    "status": "success",
                    "operation": route,
                    "request_id": attribution_ctx.request_id,
                    "consumer_ref": attribution_ctx.consumer_ref,
                    "data_available": data_result.available,
                },
            )
            

            semantic_response = self.semantics.annotate(policy_decision = policy_decision ,data_result= data_result)

            latency_ms = (time.perf_counter() - start) * 1000

            logger.info(
                "API request completed",
                extra={
                    "service": "api-service",
                    "event": "api.request.completed",
                    "status": "success",
                    "operation": route,
                    "request_id": attribution_ctx.request_id,
                    "consumer_ref": attribution_ctx.consumer_ref,
                    "consumer_type": attribution_ctx.consumer_type,
                    "path": attribution_ctx.path,
                    "method": attribution_ctx.method,
                    "policy_decision": policy_decision.decision.name,
                    "data_available": data_result.available,
                    "semantic_type": semantic_response.type,
                    "semantic_msg": semantic_response.message,
                    "latency_ms": latency_ms,
                },
            )

            return semantic_response
        
        except Exception:
            latency_ms = (time.perf_counter() - start) * 1000

            logger.exception(
                "API request failed",
                extra={
                    "service": "api-service",
                    "event": "api.request.failed",
                    "status": "error",
                    "operation": route,
                    "request_id": getattr(attribution_ctx, "request_id", None),
                    "consumer_ref": getattr(attribution_ctx, "consumer_ref", None),
                    "path": getattr(request.url, "path", None),
                    "method": getattr(request, "method", None),
                    "latency_ms": latency_ms,
                },
            )

            raise        