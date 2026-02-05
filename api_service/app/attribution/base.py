from dataclasses import dataclass

@dataclass
class AttributionContext:
    """Context شناسه‌ی درخواست، consumer و سایر متادیتای درخواست را نگه می‌دارد."""
    request_id: str
    consumer_tier: str
    source_ip: str


class AttributionResolver:
    """هر درخواست باید بدانیم از چه کسی آمده است."""
    def resolve(self, request) -> AttributionContext:
        raise NotImplementedError
