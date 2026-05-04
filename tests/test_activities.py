"""
Tests for the Mergington High School Activities API

This module contains comprehensive tests for all API endpoints using the AAA (Arrange-Act-Assert) pattern.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """Return the expected structure of activities data."""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }


class TestGetActivities:
    """Test cases for GET /activities endpoint."""

    def test_get_activities_success(self, client, sample_activities):
        """Test successful retrieval of all activities."""
        # Arrange - Set up test expectations
        expected_keys = ["description", "schedule", "max_participants", "participants"]

        # Act - Make the API call
        response = client.get("/activities")

        # Assert - Verify the response
        assert response.status_code == 200
        activities = response.json()

        # Check that we have activities returned
        assert isinstance(activities, dict)
        assert len(activities) > 0

        # Check structure of first activity
        first_activity = next(iter(activities.values()))
        for key in expected_keys:
            assert key in first_activity

        # Check that participants is a list
        assert isinstance(first_activity["participants"], list)


class TestSignupForActivity:
    """Test cases for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client):
        """Test successful signup for an activity."""
        # Arrange - Prepare test data
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act - Make the signup request
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert - Verify the response
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email in result["message"]
        assert activity_name in result["message"]

    def test_signup_activity_not_found(self, client):
        """Test signup for non-existent activity."""
        # Arrange - Use invalid activity name
        invalid_activity = "NonExistent Club"
        email = "student@mergington.edu"

        # Act - Attempt signup
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": email}
        )

        # Assert - Verify error response
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "Activity not found" in result["detail"]

    def test_signup_duplicate_participant(self, client):
        """Test signup when student is already registered."""
        # Arrange - Use email that's already in Chess Club
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"

        # Act - Attempt duplicate signup
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )

        # Assert - Verify error response
        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "already signed up" in result["detail"]


class TestUnregisterParticipant:
    """Test cases for DELETE /activities/{activity_name}/participants endpoint."""

    def test_unregister_success(self, client):
        """Test successful removal of a participant."""
        # Arrange - Use existing participant
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"

        # Act - Make the delete request
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email_to_remove}
        )

        # Assert - Verify the response
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email_to_remove in result["message"]
        assert activity_name in result["message"]
        assert "Unregistered" in result["message"]

    def test_unregister_activity_not_found(self, client):
        """Test unregister from non-existent activity."""
        # Arrange - Use invalid activity name
        invalid_activity = "NonExistent Club"
        email = "student@mergington.edu"

        # Act - Attempt unregister
        response = client.delete(
            f"/activities/{invalid_activity}/participants",
            params={"email": email}
        )

        # Assert - Verify error response
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "Activity not found" in result["detail"]

    def test_unregister_participant_not_found(self, client):
        """Test unregister when participant is not in the activity."""
        # Arrange - Use valid activity but email not in it
        activity_name = "Chess Club"
        non_participant_email = "notregistered@mergington.edu"

        # Act - Attempt unregister
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": non_participant_email}
        )

        # Assert - Verify error response
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "Participant not found" in result["detail"]


class TestRootEndpoint:
    """Test cases for GET / endpoint."""

    def test_root_redirect(self, client):
        """Test that root endpoint redirects to static index."""
        # Arrange - No special setup needed

        # Act - Make request to root
        response = client.get("/")

        # Assert - Verify redirect response
        assert response.status_code == 200  # FastAPI handles redirect internally in test client
        # Note: In real server, this would be 302, but TestClient follows redirects