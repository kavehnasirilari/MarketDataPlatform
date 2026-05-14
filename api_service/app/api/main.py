# api_service/app/api/main.py
import logging
from typing import Optional
from fastapi import FastAPI, Request
from api_service.app.api.flow.execution import ExecutionOrchestrator
from api_service.app.attribution.http_impl import HttpAttributionResolver
from api_service.app.policy.mock_impl import MockPolicyEngine
from api_service.app.dataAccess.mock_impl import MockDataAccessor, MockMetaDataAccessor
from api_service.app.semantics.mock_impl import MockSemanticAnnotator
from api_service.app.observability.logging_config import configure_logging

configure_logging()


# فقط app خودت
logging.getLogger("app").setLevel(logging.INFO)

# بستن کامل نویز
for name in list(logging.root.manager.loggerDict.keys()):
    if name.startswith("sqlalchemy"):
        l = logging.getLogger(name)
        l.handlers.clear()
        l.propagate = False
        l.disabled = True


app = FastAPI()

orchestrator = ExecutionOrchestrator(
    attribution=HttpAttributionResolver(),
    policy=MockPolicyEngine(),
    data=MockDataAccessor(),
    metadata=MockMetaDataAccessor(),
    semantics=MockSemanticAnnotator(),
)

@app.get("/health")
async def health_check():
    return {
        "type": "success",
        "message": None,
        "data": {
            "status": "ok"
        },
    }

@app.get("/candles/{exchange}/{market}/{symbol}/{interval}")
async def get_candles(
    request: Request, 
    exchange: str,
    market: str, 
    symbol: str, 
    interval: str, 
    limit: int = 100
):
    payload = {
        "exchange": exchange,
        "market": market,
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    result = orchestrator.handle_request(
        request=request,
        route="gat_candle",
        payload=payload
    )
    return result

@app.get("/metadata")
async def get_metadata(
    request: Request,
    exchange: Optional[str] = None,
    market: Optional[str] = None,
    symbol: Optional[str] = None,
    interval: Optional[str] = None
    ):

    payload = {
        "exchange": exchange,
        "market": market,
        "symbol": symbol,
        "interval": interval
    }

    result = orchestrator.handle_request(
        request=request,
        route="get_metadata",
        payload=payload
    )
    return result
