# api_service/app/attribution/http_impl.py
from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Optional, Tuple

from api_service.app.attribution.base import AttributionResolver, AttributionContext


class HttpAttributionResolver(AttributionResolver):
    """
    Builds AttributionContext from an incoming HTTP request.
    Attribution only (tracking), NOT authentication/validation.
    """

    def __init__(
        self,
        request_id_header: str = "X-Request-ID",
        api_key_header: str = "X-API-Key",
        forwarded_for_header: str = "X-Forwarded-For",
        real_ip_header: str = "X-Real-IP",
    ) -> None:
        self.request_id_header = request_id_header
        self.api_key_header = api_key_header
        self.forwarded_for_header = forwarded_for_header
        self.real_ip_header = real_ip_header

    def resolve(self, request) -> AttributionContext:
        request_id = self._get_request_id(request)
        source_ip, ip_source = self._get_source_ip(request)

        path = getattr(getattr(request, "url", None), "path", "") or ""
        method = getattr(request, "method", "") or ""
        user_agent = self._header(request, "user-agent")

        api_key_raw = self._header(request, self.api_key_header)

        received_at = datetime.now(timezone.utc)

        if api_key_raw:
            fingerprint = self._fingerprint(api_key_raw)
            consumer_type = "registered"
            consumer_ref = f"key:{fingerprint}"
            api_key_fingerprint = fingerprint
        else:
            consumer_type = "public"
            consumer_ref = f"ip:{source_ip}"
            api_key_fingerprint = None

        return AttributionContext(
            request_id=request_id,
            source_ip=source_ip,
            ip_source=ip_source,
            consumer_type=consumer_type,
            consumer_ref=consumer_ref,
            consumer_id=None,
            api_key_id=None,
            api_key_fingerprint=api_key_fingerprint,
            path=path,
            method=method,
            user_agent=user_agent,
            received_at=received_at,
        )

    # ---------------- helpers ----------------

    def _get_request_id(self, request) -> str:
        rid = self._header(request, self.request_id_header)
        return rid.strip() if rid and rid.strip() else str(uuid.uuid4())

    def _get_source_ip(self, request) -> Tuple[str, str]:
        """
        Priority:
          1) X-Forwarded-For (first IP)
          2) X-Real-IP
          3) request.client.host
        """
        xff = self._header(request, self.forwarded_for_header)
        if xff:
            first = self._first_ip_from_xff(xff)
            if first:
                return first, "x-forwarded-for"

        xri = self._header(request, self.real_ip_header)
        if xri and xri.strip():
            return xri.strip(), "x-real-ip"

        client = getattr(request, "client", None)
        host = getattr(client, "host", None) if client else None
        return (host or "unknown"), "direct"

    @staticmethod
    def _first_ip_from_xff(xff_value: str) -> Optional[str]:
        # Example: "1.2.3.4, 5.6.7.8"
        parts = [p.strip() for p in xff_value.split(",") if p.strip()]
        return parts[0] if parts else None

    @staticmethod
    def _fingerprint(api_key_raw: str) -> str:
        # short, stable, non-reversible fingerprint
        digest = hashlib.sha256(api_key_raw.encode("utf-8")).hexdigest()
        return digest[:12]  # keep short for logs

    @staticmethod
    def _header(request, name: str) -> Optional[str]:
        headers = getattr(request, "headers", None)
        if not headers:
            return None
        # Starlette headers are case-insensitive for .get()
        return headers.get(name)
