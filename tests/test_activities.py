"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_all_activities(client):
    """
    Arrange: No setup needed (activities are pre-populated)
    Act: Make a GET request to /activities
    Assert: Verify all activities are returned
    """
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Soccer Club",
        "Art Club",
        "Drama Club",
        "Debate Club",
        "Science Club"
    ]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    # Verify it's a dictionary
    assert isinstance(data, dict)
    
    # Verify all expected activities are present
    for activity in expected_activities:
        assert activity in data


def test_activity_data_structure(client):
    """
    Arrange: No setup needed
    Act: Make a GET request to /activities
    Assert: Verify each activity has the required fields
    """
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    for activity_name, activity_data in data.items():
        for field in required_fields:
            assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"


def test_activity_participants_is_list(client):
    """
    Arrange: No setup needed
    Act: Make a GET request to /activities
    Assert: Verify participants field is a list
    """
    # Arrange - No setup needed
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    for activity_name, activity_data in data.items():
        assert isinstance(activity_data["participants"], list), \
            f"Activity '{activity_name}' participants should be a list"


def test_activity_max_participants_is_integer(client):
    """
    Arrange: No setup needed
    Act: Make a GET request to /activities
    Assert: Verify max_participants is an integer
    """
    # Arrange - No setup needed
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    for activity_name, activity_data in data.items():
        assert isinstance(activity_data["max_participants"], int), \
            f"Activity '{activity_name}' max_participants should be an integer"


def test_get_activities_returns_json(client):
    """
    Arrange: No setup needed
    Act: Make a GET request to /activities
    Assert: Verify response is valid JSON
    """
    # Arrange - No setup needed
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
