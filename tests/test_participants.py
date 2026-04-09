"""
Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint.
"""

import pytest


def test_remove_participant_success(client):
    """
    Arrange: Sign up a student for an activity
    Act: Make a DELETE request to remove the participant
    Assert: Verify successful removal response
    """
    # Arrange
    activity_name = "Basketball Team"
    student_email = "basketball_student@mergington.edu"
    
    # First sign up the student
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{student_email}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert student_email in data["message"]
    assert activity_name in data["message"]


def test_remove_participant_deletes_from_list(client):
    """
    Arrange: Sign up a student for an activity
    Act: Make a DELETE request, then GET /activities
    Assert: Verify the student was removed from the participants list
    """
    # Arrange
    activity_name = "Soccer Club"
    student_email = "soccer_student@mergington.edu"
    
    # First sign up the student
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Verify student is in the list
    activities_before = client.get("/activities").json()
    assert student_email in activities_before[activity_name]["participants"]
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{student_email}"
    )
    
    # Assert
    assert response.status_code == 200
    
    # Verify student is no longer in the list
    activities_after = client.get("/activities").json()
    assert student_email not in activities_after[activity_name]["participants"]


def test_remove_nonexistent_participant_fails(client):
    """
    Arrange: Try to remove a student who is not signed up
    Act: Make a DELETE request for a non-existent participant
    Assert: Verify the request fails with 404 status
    """
    # Arrange
    activity_name = "Art Club"
    nonexistent_student = "nonexistent_student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{nonexistent_student}"
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower() or "not signed up" in data["detail"].lower()


def test_remove_from_nonexistent_activity_fails(client):
    """
    Arrange: Try to remove a student from an activity that doesn't exist
    Act: Make a DELETE request to a non-existent activity
    Assert: Verify the request fails with 404 status
    """
    # Arrange
    nonexistent_activity = "Nonexistent Activity"
    student_email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{nonexistent_activity}/participants/{student_email}"
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_remove_participant_returns_json(client):
    """
    Arrange: Sign up a student for an activity
    Act: Make a DELETE request to remove the participant
    Assert: Verify response is valid JSON
    """
    # Arrange
    activity_name = "Drama Club"
    student_email = "drama_removal@mergington.edu"
    
    # First sign up the student
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{student_email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert isinstance(response.json(), dict)


def test_remove_with_url_encoded_activity_name(client):
    """
    Arrange: Sign up student for activity with spaces in name
    Act: Make DELETE request with URL-encoded activity name
    Assert: Verify removal works with URL encoding
    """
    # Arrange
    activity_name = "Debate Club"
    student_email = "debate_removal@mergington.edu"
    
    # Sign up the student
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Act
    response = client.delete(
        f"/activities/Debate%20Club/participants/{student_email}"
    )
    
    # Assert
    assert response.status_code == 200


def test_remove_with_url_encoded_email(client):
    """
    Arrange: Sign up student with special characters in email
    Act: Make DELETE request with URL-encoded email
    Assert: Verify removal works with URL encoding
    """
    # Arrange
    activity_name = "Science Club"
    student_email = "science+student@mergington.edu"
    
    # Sign up the student
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/science%2Bstudent%40mergington.edu"
    )
    
    # Assert
    assert response.status_code == 200
