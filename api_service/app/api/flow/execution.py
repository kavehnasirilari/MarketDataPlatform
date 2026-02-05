import logging
from api_service.app.attribution.base import AttributionResolver
from api_service.app.policy.base import PolicyEngine, PolicyDecisionType
from api_service.app.dataAccess.base import DataAccessor
from api_service.app.semantics.base import SemanticAnnotator

logger = logging.getLogger(__name__)

class ExecutionOrchestrator:
    """مدیریت جریان اجرای درخواست از ورودی تا خروجی"""

    def __init__(
        self,
        attribution: AttributionResolver,
        policy: PolicyEngine,
        data: DataAccessor,
        semantics: SemanticAnnotator,
    ):
        self.attribution = attribution
        self.policy = policy
        self.data = data
        self.semantics = semantics

    def handle_request(self, request):
        logger.info("Execution started", extra={"path": request.url.path})


        attribution_ctx = self.attribution.resolve(request)

        logger.info("Attribution resolved", extra={"attr": attribution_ctx.__dict__})

        policy_decision = self.policy.evaluate(attribution_ctx, request)
        logger.info("Policy evaluated", extra={"decision": policy_decision.decision})


        if policy_decision.decision != PolicyDecisionType.ALLOW:
            semantic = self.semantics.annotate(
                policy_decision=policy_decision
            )
            logger.info("Execution completed (policy rejection)")
            return semantic

        data_result = self.data.fetch(request)
        logger.info("Data fetched", extra={"available": data_result.available})

        semantic_response = self.semantics.annotate(policy_decision = policy_decision ,data_result= data_result)
        logger.info("Semantics applied")

        logger.info("Execution completed")
        return semantic_response
