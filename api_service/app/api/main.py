# api/main.py
import logging
from fastapi import FastAPI, Request
from api_service.app.api.flow.execution import ExecutionOrchestrator
from api_service.app.attribution.mock_impl import MockAttributionResolver
from api_service.app.policy.mock_impl import MockPolicyEngine
from api_service.app.dataAccess.mock_impl import MockDataAccessor
from api_service.app.semantics.mock_impl import MockSemanticAnnotator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


app = FastAPI()

orchestrator = ExecutionOrchestrator(
    attribution=MockAttributionResolver(),
    policy=MockPolicyEngine(),
    data=MockDataAccessor(),
    semantics=MockSemanticAnnotator(),
)

@app.get("/health")
async def health_check(request: Request):
    result = orchestrator.handle_request(request)
    return result
