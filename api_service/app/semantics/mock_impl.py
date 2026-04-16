#api_service/app/semantics/mock_impl.py

from api_service.app.semantics.base import SemanticType, SemanticResult, SemanticAnnotator
from api_service.app.policy.base import PolicyDecisionType

class MockSemanticAnnotator(SemanticAnnotator):
    def annotate(self, policy_decision=None, data_result=None) -> SemanticResult:

        if policy_decision.decision == PolicyDecisionType.DENY:
            return SemanticResult(
                type = SemanticType.ERROR.value,
                message= policy_decision.reason
            )

        if data_result.available == False:      
            return SemanticResult(
                 type = SemanticType.ERROR.value,
                message= data_result.message
            )        
        
        return SemanticResult(
            type = SemanticType.SUCCESS.value,
            message= None,
            data= data_result.payload
        ) 



