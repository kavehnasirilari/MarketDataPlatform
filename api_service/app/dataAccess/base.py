#api_service/app/dataAccess/base.py

from dataclasses import dataclass

@dataclass
class DataResault:
    available: bool
    message: str
    payload: object | None = None

@dataclass
class MetadataResult:
    available: bool
    message: str | None = None
    payload: object | None = None

class DataAccessor:
    def fetch(self, request, payload: dict) -> DataResault:
        raise NotImplemented

class MetadataAccessor:
    def fetch(self, request, payload: dict) -> MetadataResult:
        raise NotImplemented