"""
Tests for the user API endpoints.
"""
import pytest
from fastapi.testclient import TestClient


def test_create_user(client):
    """
    Test creating a new user.
    
    Verifies that the user creation endpoint returns the correct response with a 201 status code.
    """
    # Test user data
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "role": "tester"
    }
    
    # Send POST request to create user
    response = client.post("/users", json=user_data)
    
    # Assert status code is 201 Created
    assert response.status_code == 201
    
    # Assert the response contains the expected fields
    data = response.json()
    assert "id" in data
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert data["role"] == user_data["role"]
    
    # Store the user ID for later tests
    return data["id"]


def test_get_users(client):
    """
    Test getting all users.
    
    Verifies that the get users endpoint returns a list of users with a 200 status code.
    """
    # Create a test user first
    test_create_user(client)
    
    # Send GET request to get all users
    response = client.get("/users")
    
    # Assert status code is 200 OK
    assert response.status_code == 200
    
    # Assert the response is a list
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # Assert user fields are present
    user = data[0]
    assert "id" in user
    assert "name" in user
    assert "email" in user
    assert "role" in user


def test_get_user_by_id(client):
    """
    Test getting a specific user by ID.
    
    Verifies that the get user by ID endpoint returns the correct user with a 200 status code.
    """
    # Create a test user and get the ID
    user_id = test_create_user(client)
    
    # Send GET request to get the user by ID
    response = client.get(f"/users/{user_id}")
    
    # Assert status code is 200 OK
    assert response.status_code == 200
    
    # Assert the response contains the correct user
    data = response.json()
    assert data["id"] == user_id
    assert "name" in data
    assert "email" in data
    assert "role" in data


def test_get_nonexistent_user(client):
    """
    Test getting a nonexistent user.
    
    Verifies that the API returns a 404 status code when requesting a nonexistent user.
    """
    # Send GET request for a nonexistent user
    response = client.get("/users/nonexistent-id")
    
    # Assert status code is 404 Not Found
    assert response.status_code == 404
    
    # Assert the response contains an error detail
    data = response.json()
    assert "detail" in data


def test_duplicate_email(client):
    """
    Test creating a user with a duplicate email.
    
    Verifies that the API returns a 400 status code when attempting to create a user with an email
    that already exists.
    """
    # Test user data
    user_data = {
        "name": "Duplicate User",
        "email": "duplicate@example.com",
        "role": "tester"
    }
    
    # Create the first user
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    
    # Try to create a second user with the same email
    response = client.post("/users", json=user_data)
    
    # Assert status code is 400 Bad Request
    assert response.status_code == 400
    
    # Assert the response contains an error detail
    data = response.json()
    assert "detail" in data