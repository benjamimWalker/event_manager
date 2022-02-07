import pytest
from starlette.testclient import TestClient
from load import app


@pytest.fixture
def my_client() -> TestClient:
    return TestClient(app)
