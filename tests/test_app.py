from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # expect at least one activity
    assert len(data) > 0


def test_signup_and_prevent_duplicate():
    activity = "Chess Club"
    email = "teststudent@mergington.edu"

    # Ensure email is not present initially; if present, remove it
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup should succeed
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail with 400
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400


def test_remove_participant():
    activity = "Chess Club"
    email = "teststudent@mergington.edu"

    # Ensure email is present
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)

    # Delete the participant
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]
