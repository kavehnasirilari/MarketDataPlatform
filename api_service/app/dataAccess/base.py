#api_service/app/dataAccess/base.py

from dataclasses import dataclass

@dataclass
class DataResault:
    available: bool
    payload: object | None = None

class DataAccessor:
    def fetch(self, request) -> DataResault:
        raise NotImplemented