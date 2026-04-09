"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_signup_success(client):
    """
    Arrange: A valid activity and a new student email
    Act: Make a POST request to signup
    Assert: Verify successful signup response
    """
    # Arrange
    activity_name = "Chess Club"
    new_student_email = "new_student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_student_email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert new_student_email in data["message"]
    assert activity_name in data["message"]


def test_signup_adds_participant(client):
    """
    Arrange: A valid activity and a new student email
    Act: Make a POST request to signup, then GET /activities
    Assert: Verify the student was added to the participants list
    """
    # Arrange
    activity_name = "Programming Class"
    new_student_email = "new_programmer@mergington.edu"
    
    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_student_email}
    )
    
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    
    # Assert
    assert signup_response.status_code == 200
    assert new_student_email in activities_data[activity_name]["participants"]


def test_signup_duplicate_student_fails(client):
    """
    Arrange: Sign up a student, then try to sign up the same student again
    Act: Make a second POST request with the same email
    Assert: Verify the second signup fails with 400 status
    """
    # Arrange
    activity_name = "Gym Class"
    student_email = "duplicate_student@mergington.edu"
    
    # First signup - should succeed
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Act
    # Try to signup the same student again
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 400
    data = response2.json()
    assert "already signed up" in data["detail"].lower() or "already" in data["detail"].lower()


def test_signup_nonexistent_activity_fails(client):
    """
    Arrange: Try to signup for an activity that doesn't exist
    Act: Make a POST request with a non-existent activity name
    Assert: Verify the request fails with 404 status
    """
    # Arrange
    nonexistent_activity = "Nonexistent Activity"
    student_email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{nonexistent_activity}/signup",
        params={"email": student_email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_signup_with_special_characters_in_email(client):
    """
    Arrange: A valid activity and an email with special characters
    Act: Make a POST request with special characters
    Assert: Verify the signup works correctly
    """
    # Arrange
    activity_name = "Art Club"
    special_email = "student+art@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": special_email}
    )
    
    # Assert
    assert response.status_code == 200
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert special_email in activities_data[activity_name]["participants"]


def test_signup_returns_json(client):
    """
    Arrange: A valid activity and student email
    Act: Make a POST request to signup
    Assert: Verify response is valid JSON
    """
    # Arrange
    activity_name = "Drama Club"
    student_email = "drama_student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert isinstance(response.json(), dict)


def test_signup_with_url_encoded_activity_name(client):
    """
    Arrange: An activity with spaces in the name that needs URL encoding
    Act: Make a POST request with properly encoded activity name
    Assert: Verify signup works with URL encoding
    """
    # Arrange
    activity_name = "Chess Club"  # Activity exists with this name
    student_email = "chess_student@mergington.edu"
    
    # Act
    # URL encode the activity name (Chess Club becomes Chess%20Club)
    response = client.post(
        f"/activities/Chess%20Club/signup",
        params={"email": student_email}
    )
    
    # Assert
    assert response.status_code == 200


def test_signup_activity_at_capacity_fails(client):
    """
    Arrange: Fill an activity to maximum capacity, then try to add one more student
    Act: Make a POST request to signup for a full activity
    Assert: Verify the request fails with 400 status
    """
    # Arrange
    activity_name = "Chess Club"  # Max 12 participants
    base_participants = ["test1@mergington.edu", "test2@mergington.edu"]  # Already has 2
    
    # Fill the activity to capacity (12 total)
    for i in range(10):  # Add 10 more to reach 12
        email = f"capacity_test{i}@mergington.edu"
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
    
    # Verify we're at capacity
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert len(activities_data[activity_name]["participants"]) == 12
    
    # Act - Try to add one more student
    extra_student = "extra_student@mergington.edu"
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": extra_student}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "capacity" in data["detail"].lower() or "full" in data["detail"].lower()
