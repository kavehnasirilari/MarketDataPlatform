#api_service/app/policy/base.py

from enum import Enum
from dataclasses import dataclass

class PolicyDecisionType(Enum):
    ALLOW = "allow"
    DENY = "deny"
    LIMIT = "limit"


@dataclass
class PolicyDecision:
    decision: PolicyDecisionType
    reason: str | None = None

class PolicyEngine:
    def evaluate(self,snapshot, attribution_ctx, request) -> PolicyDecision:
        raise NotImplemented
    



