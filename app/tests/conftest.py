"""
Pytest configuration file.
Contains fixtures and configuration for testing the API.
"""
import pytest
from fastapi.testclient import TestClient
import os
import sys

# Add the parent directory to sys.path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

@pytest.fixture
def client():
    """
    Test client fixture.
    
    Returns:
        TestClient: A FastAPI test client for making requests to the API
    """
    with TestClient(app) as test_client:
        yield test_client