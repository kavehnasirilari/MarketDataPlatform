from __future__ import annotations

from typing import Iterable, List, Optional

from sqlalchemy.orm import Session

from database.models import (
    SupportedMarket,
    ExchangeMarket,
    Exchange,
    Interval,
    CanonicalSymbol,
)

from syncer_service.syncer.ingestion.types import IngestionUnit


def load_ingestion_units(
    session: Session,
    *,
    supported_market_ids: Optional[Iterable[int]] = None,
    interval_ids: Optional[Iterable[int]] = None,
    only_active: bool = True,
) -> List[IngestionUnit]:
    """
    Load ingestion units from database metadata.

    Allowed filters (Phase 4B):
    - supported_market_ids
    - interval_ids

    This function:
    - does NOT manage session lifecycle
    - does NOT fetch candles
    - does NOT apply incremental logic
    """

    query = (
        session.query(
            SupportedMarket.id.label("supported_market_id"),
            ExchangeMarket.id.label("exchange_market_id"),
            Interval.id.label("interval_id"),
            Exchange.name.label("exchange_name"),
            ExchangeMarket.market_type.label("market_type"),
            CanonicalSymbol.symbol.label("canonical_symbol"),
            Interval.interval.label("interval"),   # ✅ اصلاح شد
            Interval.ms.label("interval_ms"),
        )
        .join(ExchangeMarket, SupportedMarket.exchange_market_id == ExchangeMarket.id)
        .join(Exchange, ExchangeMarket.exchange_id == Exchange.id)
        .join(Interval, SupportedMarket.interval_id == Interval.id)
        .join(CanonicalSymbol, ExchangeMarket.canonical_symbol_id == CanonicalSymbol.id)
    )

    if only_active:
        query = query.filter(
            SupportedMarket.status == "active",
        )

    # -----------------------
    # Primitive filters ONLY
    # -----------------------

    if supported_market_ids is not None:
        supported_market_ids = list(supported_market_ids)
        if supported_market_ids:
            query = query.filter(SupportedMarket.id.in_(supported_market_ids))
        else:
            return []

    if interval_ids is not None:
        interval_ids = list(interval_ids)
        if interval_ids:
            query = query.filter(Interval.id.in_(interval_ids))
        else:
            return []

    rows = query.all()

    return [
        IngestionUnit(
            supported_market_id=row.supported_market_id,
            exchange_market_id=row.exchange_market_id,
            interval_id=row.interval_id,
            exchange_name=row.exchange_name,
            market_type=row.market_type,
            canonical_symbol=row.canonical_symbol,
            interval=row.interval,          # string مثل "1m", "5m"
            interval_ms=row.interval_ms,
        )
        for row in rows
    ]
