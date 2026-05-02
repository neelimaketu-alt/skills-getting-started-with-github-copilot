def test_signup_successful(client):
    """Test successful signup for an activity."""
    response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    result = response.json()
    assert result["message"] == "Signed up newstudent@mergington.edu for Chess Club"

    # Verify the participant was added
    resp = client.get("/activities")
    chess_club = resp.json()["Chess Club"]
    assert "newstudent@mergington.edu" in chess_club["participants"]


def test_signup_invalid_activity(client):
    """Test signup for non-existent activity."""
    response = client.post("/activities/NonExistent Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    result = response.json()
    assert result["detail"] == "Activity not found"


def test_signup_duplicate(client):
    """Test attempting to sign up for an activity twice."""
    email = "duplicate@mergington.edu"
    activity = "Programming Class"

    # First signup should succeed
    response1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response1.status_code == 200

    # Second signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    result = response2.json()
    assert result["detail"] == "Student already signed up for this activity"


def test_signup_max_participants_not_exceeded(client):
    """Test that signup works when not at max capacity."""
    # Basketball Team has max 15, currently 1 participant
    response = client.post("/activities/Basketball Team/signup?email=extra@mergington.edu")
    assert response.status_code == 200

    # Verify added
    resp = client.get("/activities")
    basketball = resp.json()["Basketball Team"]
    assert "extra@mergington.edu" in basketball["participants"]
    assert len(basketball["participants"]) == 2