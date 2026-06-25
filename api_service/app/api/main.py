# api_service/app/api/main.py
import logging
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import Response
from contextlib import asynccontextmanager
from api_service.app.api.flow.execution import ExecutionOrchestrator
from api_service.app.attribution.http_impl import HttpAttributionResolver
from api_service.app.policy.mock_impl import MockPolicyEngine
from api_service.app.dataAccess.mock_impl import MockDataAccessor, MockMetaDataAccessor
from api_service.app.semantics.mock_impl import MockSemanticAnnotator
from core.observability.logging_config import configure_logging

configure_logging()

logger = logging.getLogger(__name__)
# فقط app خودت
logging.getLogger("app").setLevel(logging.INFO)

# بستن کامل نویز
for name in list(logging.root.manager.loggerDict.keys()):
    if name.startswith("sqlalchemy"):
        sqlalchemy_logger = logging.getLogger(name)
        sqlalchemy_logger.handlers.clear()
        sqlalchemy_logger.propagate = False
        sqlalchemy_logger.disabled = True

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "API service started",
        extra={
            "service": "api-service",
            "event": "api.service.started",
            "status": "success",
            "operation": "startup",
        },
    )

    yield

    logger.info(
        "API service stopped",
        extra={
            "service": "api-service",
            "event": "api.service.stopped",
            "status": "success",
            "operation": "shutdown",
        },
    )


app = FastAPI(lifespan=lifespan)

orchestrator = ExecutionOrchestrator(
    attribution=HttpAttributionResolver(),
    policy=MockPolicyEngine(),
    data=MockDataAccessor(),
    metadata=MockMetaDataAccessor(),
    semantics=MockSemanticAnnotator(),
)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)


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
        route="get_candles",
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
