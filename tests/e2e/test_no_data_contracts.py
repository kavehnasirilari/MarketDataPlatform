import requests
import pytest

BASE_URL = "http://localhost:8000"


def test_valid_metadata_filter_with_no_matching_data_returns_success_empty_result():
    response = requests.get(
        f"{BASE_URL}/metadata?exchange=binance&market_type=futures&symbol=NO-DATA-SYMBOL&interval=1m",
        timeout=10,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["type"] == "error"
    assert body["message"] is None
    assert body["data"] is None



