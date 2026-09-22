def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_structure(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    chess_club = activities["Chess Club"]
    assert set(chess_club.keys()) == {
        "description", "schedule", "max_participants", "participants"
    }


def test_signup_for_activity_success(client):
    response = client.post(
        "/activities/Chess Club/signup?email=new-student@mergington.edu"
    )

    assert response.status_code == 200
    assert "new-student@mergington.edu" in response.json()["message"]

    activities = client.get("/activities").json()
    assert "new-student@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_for_nonexistent_activity_returns_404(client):
    response = client.post(
        "/activities/Not A Real Club/signup?email=student@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_when_already_registered_returns_400(client):
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()[
        "detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_email(client):
    signup = client.post(
        "/activities/Chess Club/signup?email=test@mergington.edu"
    )
    assert signup.status_code == 200

    response = client.delete(
        "/activities/Chess Club/participants/test@mergington.edu"
    )

    assert response.status_code == 200
    assert "test@mergington.edu" in response.json()["message"]

    activities = client.get("/activities").json()
    assert "test@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_from_nonexistent_activity_returns_404(client):
    response = client.delete(
        "/activities/Not A Real Club/participants/student@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_not_found_returns_404(client):
    response = client.delete(
        "/activities/Chess Club/participants/not-signed-up@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()[
        "detail"] == "Participant not found in this activity"
