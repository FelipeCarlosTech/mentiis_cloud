"""
Tests for the health check endpoints.
"""
import pytest
from fastapi.testclient import TestClient


def test_health_endpoint(client):
    """
    Test the health check endpoint.
    
    Verifies that the health endpoint returns the correct response and status code.
    """
    response = client.get("/health")
    
    # Assert status code is 200 OK
    assert response.status_code == 200
    
    # Assert the response contains the expected fields
    data = response.json()
    assert "status" in data
    assert "version" in data
    
    # Assert the values are as expected
    assert data["status"] == "healthy"
    assert isinstance(data["version"], str)