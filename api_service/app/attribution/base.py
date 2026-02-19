from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class AttributionContext:
    """Context شناسه‌ی درخواست، consumer و سایر متادیتای درخواست را نگه می‌دارد."""
    request_id: str
    source_ip: str
    ip_source: str # direct | x-forwarded-for | x-real-ip
    consumer_type: str # public | registered
    consumer_ref: str
    consumer_id: Optional[int] = None
    api_key_id: Optional[int] = None
    api_key_fingerprint: Optional [str] = None # never log raw key

    path: str = ""
    method: str = ""
    user_agent: Optional [str] = None
    received_at: Optional [datetime] = None


class AttributionResolver:
    """هر درخواست باید بدانیم از چه کسی آمده است."""
    def resolve(self, request) -> AttributionContext:
        raise NotImplementedError
