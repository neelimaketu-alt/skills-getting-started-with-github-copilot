def test_delete_signup_successful(client):
    """Test successful removal from an activity."""
    email = "removeme@mergington.edu"
    activity = "Tennis Club"

    # First sign up
    client.post(f"/activities/{activity}/signup?email={email}")

    # Then remove
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    result = response.json()
    assert result["message"] == f"Removed {email} from {activity}"

    # Verify removed
    resp = client.get("/activities")
    tennis_club = resp.json()["Tennis Club"]
    assert email not in tennis_club["participants"]


def test_delete_signup_not_signed_up(client):
    """Test attempting to remove a student who is not signed up."""
    response = client.delete("/activities/Chess Club/signup?email=notsigned@mergington.edu")
    assert response.status_code == 400
    result = response.json()
    assert result["detail"] == "Student not signed up for this activity"


def test_delete_signup_invalid_activity(client):
    """Test removal from non-existent activity."""
    response = client.delete("/activities/NonExistent Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    result = response.json()
    assert result["detail"] == "Activity not found"


def test_delete_signup_multiple_removals(client):
    """Test removing multiple participants from the same activity."""
    activity = "Art Studio"
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"

    # Sign up both
    client.post(f"/activities/{activity}/signup?email={email1}")
    client.post(f"/activities/{activity}/signup?email={email2}")

    # Remove both
    client.delete(f"/activities/{activity}/signup?email={email1}")
    client.delete(f"/activities/{activity}/signup?email={email2}")

    # Verify both removed
    resp = client.get("/activities")
    art_studio = resp.json()["Art Studio"]
    assert email1 not in art_studio["participants"]
    assert email2 not in art_studio["participants"]
    # Should only have the original participant
    assert len(art_studio["participants"]) == 1