#api_service/app/dataAccess/mock_impl.py

from api_service.app.dataAccess.base import DataResault, DataAccessor

class MockDataAccessor(DataAccessor):
    def fetch(self, request) -> DataResault:
        return DataResault(
            available= False,
            payload= None
        )
