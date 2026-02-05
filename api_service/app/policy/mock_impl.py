from api_service.app.policy.base import PolicyDecisionType, PolicyDecision, PolicyEngine


class MockPolicyEngine(PolicyEngine):
    def evaluate(self, attribution_ctx, request) -> PolicyDecision :
        return PolicyDecision(
            decision= PolicyDecisionType.ALLOW,
            reason= None
        )

