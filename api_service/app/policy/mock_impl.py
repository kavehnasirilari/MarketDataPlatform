from api_service.app.policy.base import PolicyDecisionType, PolicyDecision, PolicyEngine


class MockPolicyEngine(PolicyEngine):
    def evaluate(self,snapshot, attribution_ctx, request) -> PolicyDecision :

        if snapshot.consumed_units > 3:
            return PolicyDecision(
                decision=PolicyDecisionType.DENY,
                reason= f"rate limit exceeded for consumer_ref={snapshot.consumer_ref}"
            )


        return PolicyDecision(
            decision= PolicyDecisionType.ALLOW,
            reason= 'noosh jan'
        )

