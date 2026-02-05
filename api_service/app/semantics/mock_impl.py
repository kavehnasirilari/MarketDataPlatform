#api_service/app/semantics/mock_impl.py

from api_service.app.semantics.base import SemanticType, SemanticResult, SemanticAnnotator


class MockSemanticAnnotator(SemanticAnnotator):
    def annotate(self, policy_decision=None, data_result=None) -> SemanticResult:
        return SemanticResult(
            type = SemanticType.SUCCESS,
            message= None,
            data= None
        ) 



