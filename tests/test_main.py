from unittest.mock import Mock  # Correct import for Mock

import pytest
from fastapi.testclient import TestClient

from src.main import app  # Assuming your app is initialized in main.py


# Define a route that will raise an unhandled exception to test the middleware
@app.get("/error")
async def error_route():
    raise ValueError("This is an unhandled test error")


@pytest.fixture
def client():
    return TestClient(app)


def test_middleware_handles_request_normally(client):
    response = client.get("/")
    assert response.status_code == 200


def test_middleware_logs_exception(client, monkeypatch):
    # Create a mock logger using a simple mock object
    mock_logger = Mock()

    # Use monkeypatch to replace the logger with a mock
    monkeypatch.setattr("src.main.logger", mock_logger)

    response = client.get("/error")
    assert response.status_code == 500
    assert response.json() == {"message": "Internal Server Error"}

    # Ensure that the logger's error method was called
    assert mock_logger.error.called

    # Check that the logger's error method was called with the correct arguments
    args, kwargs = mock_logger.error.call_args
    assert "Exception occurred" in args[0]
    assert "exc_info" in kwargs
