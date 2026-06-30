from api_service.app.policy.base import PolicyDecisionType, PolicyDecision, PolicyEngine


class MockPolicyEngine(PolicyEngine):
    def evaluate(self,snapshot, attribution_ctx, request) -> PolicyDecision :

        RATE_LIMIT_PER_MINUTE = 50
        if snapshot.consumed_units > RATE_LIMIT_PER_MINUTE:
            return PolicyDecision(
                decision=PolicyDecisionType.DENY,
                reason= f"rate limit exceeded for consumer_ref={snapshot.consumer_ref}"
            )


        return PolicyDecision(
            decision= PolicyDecisionType.ALLOW,
            reason= 'noosh jan'
        )

