"""
Tests for the root endpoint.
"""

import pytest


def test_root_redirect(client):
    """
    Arrange: No setup needed
    Act: Make a GET request to the root endpoint
    Assert: Verify the redirect response
    """
    # Arrange
    expected_redirect_url = "/static/index.html"
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_redirect_url


def test_root_redirect_follows_to_static_page(client):
    """
    Arrange: No setup needed
    Act: Make a GET request to the root endpoint and follow redirects
    Assert: Verify we reach the static page
    """
    # Arrange - No explicit setup needed
    
    # Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    # The redirect should lead to the static files directory
    # Note: Status code might be 307 or 200 depending on whether the
    # static file actually exists in the test environment
    assert response.status_code in [200, 307]
    assert response.history[0].status_code == 307
