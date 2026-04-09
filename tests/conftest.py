"""
Pytest configuration and fixtures for the FastAPI application tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Provides a TestClient for making requests to the FastAPI application.
    """
    return TestClient(app)
