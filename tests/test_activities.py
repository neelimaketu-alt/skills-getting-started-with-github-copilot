def test_get_activities(client):
    """Test GET /activities returns correct structure and data."""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 8  # Based on current activities in app.py

    # Check a sample activity structure
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)
    assert len(chess_club["participants"]) == 2  # Initial participants


def test_get_activities_data_integrity(client):
    """Test that GET /activities returns expected initial data."""
    response = client.get("/activities")
    data = response.json()

    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Tennis Club", "Art Studio", "Music Band", "Science Club"
    ]
    assert set(data.keys()) == set(expected_activities)

    # Verify specific activity details
    chess_club = data["Chess Club"]
    assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
    assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
    assert chess_club["max_participants"] == 12
    assert chess_club["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]