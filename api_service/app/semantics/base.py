# api_service/app/semantics/base.py

from enum import Enum
from dataclasses import dataclass

class SemanticType(Enum):
    SUCCESS = "success"
    NO_DATA = "no_data"
    POLICY_REJECTED = "policy_rejected"
    ERROR = "error"

@dataclass
class SemanticResult:
    type: SemanticType
    message: str | None = None
    data: object | None = None

class SemanticAnnotator:
    def annotate(self, policy_decision = None, data_result = None) -> SemanticResult:
        raise NotImplementedError



