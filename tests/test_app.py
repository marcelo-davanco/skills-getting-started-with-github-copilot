from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email():
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
