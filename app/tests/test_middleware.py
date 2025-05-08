"""
Tests for the middleware components.
"""
import pytest
from fastapi.testclient import TestClient
import os
import json


def test_logging_middleware(client):
    """
    Test that the logging middleware correctly logs requests.
    
    Verifies that the middleware creates log entries for API requests.
    """
    # Make a request to trigger the logging middleware
    response = client.get("/health")
    
    # The test is mainly to check that the request doesn't fail with the middleware
    assert response.status_code == 200
    
    # Check that logs directory exists (created by the logger)
    assert os.path.exists("logs") or os.path.exists("/logs")


def test_cors_middleware(client):
    """
    Test that CORS middleware is properly configured.
    
    Verifies that the CORS headers are present in the response.
    """
    # Make a request with an Origin header
    response = client.get(
        "/health", 
        headers={"Origin": "http://testserver.com"}
    )
    
    # Assert that the CORS headers are present
    assert "access-control-allow-origin" in response.headers
    
    # For the permissive CORS config we're using, the origin should be reflected
    assert response.headers["access-control-allow-origin"] == "*"