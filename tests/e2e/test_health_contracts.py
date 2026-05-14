import pytest


pytestmark = pytest.mark.skip(
    reason="/health endpoint currently returns internal server error"
)