import uuid

from fastapi.testclient import TestClient

from app.main import app
from app.database import SessionLocal
from app.models import User, Application


client = TestClient(app)


def create_test_user():
    email = f"test_{uuid.uuid4().hex[:8]}@test.com"

    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "test123"
        }
    )

    assert response.status_code == 200

    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "test123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return email, token


def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Job Application Tracker API is running"


def test_authenticated_application_flow():
    email, token = create_test_user()

    headers = auth_headers(token)

    # CREATE
    create_response = client.post(
        "/applications/",
        json={
            "company": "Test Company",
            "role": "Software Engineer",
            "status": "Applied",
            "package": "8 LPA",
            "notes": "Automated test application"
        },
        headers=headers
    )

    assert create_response.status_code == 200

    application = create_response.json()

    application_id = application["id"]

    assert application["company"] == "Test Company"
    assert application["role"] == "Software Engineer"
    assert application["status"] == "Applied"
    assert application["is_archived"] is False

    # GET
    get_response = client.get(
        f"/applications/{application_id}",
        headers=headers
    )

    assert get_response.status_code == 200

    result = get_response.json()

    assert result["id"] == application_id
    assert result["company"] == "Test Company"

    # UPDATE
    update_response = client.put(
        f"/applications/{application_id}",
        json={
            "company": "Test Company",
            "role": "Backend Developer",
            "status": "Interview",
            "package": "10 LPA",
            "notes": "Updated by automated test"
        },
        headers=headers
    )

    assert update_response.status_code == 200

    updated = update_response.json()

    assert updated["role"] == "Backend Developer"
    assert updated["status"] == "Interview"

    # ARCHIVE
    archive_response = client.patch(
        f"/applications/{application_id}/archive",
        headers=headers
    )

    assert archive_response.status_code == 200

    assert archive_response.json()["message"] == (
        "Application archived successfully"
    )

    # Archived application should not appear in active applications
    list_response = client.get(
        "/applications/",
        headers=headers
    )

    assert list_response.status_code == 200

    active_ids = [
        application["id"]
        for application in list_response.json()
    ]

    assert application_id not in active_ids

    # ANALYTICS should still contain archived application
    analytics_response = client.get(
        "/analytics/",
        headers=headers
    )

    assert analytics_response.status_code == 200

    analytics = analytics_response.json()

    assert analytics["total_applications"] >= 1
    assert analytics["by_status"]["Interview"] >= 1

    # DELETE permanently
    delete_response = client.delete(
        f"/applications/{application_id}",
        headers=headers
    )

    assert delete_response.status_code == 200

    assert delete_response.json()["message"] == (
        "Application permanently deleted"
    )

    # Confirm deletion
    deleted_response = client.get(
        f"/applications/{application_id}",
        headers=headers
    )

    assert deleted_response.status_code == 404


def test_user_cannot_access_another_users_application():
    user1_email, user1_token = create_test_user()
    user2_email, user2_token = create_test_user()

    user1_headers = auth_headers(user1_token)
    user2_headers = auth_headers(user2_token)

    # User 1 creates an application
    create_response = client.post(
        "/applications/",
        json={
            "company": "Private Company",
            "role": "Embedded Engineer",
            "status": "Applied",
            "package": "12 LPA",
            "notes": "User 1 private application"
        },
        headers=user1_headers
    )

    assert create_response.status_code == 200

    application_id = create_response.json()["id"]

    # User 2 tries to GET User 1's application
    get_response = client.get(
        f"/applications/{application_id}",
        headers=user2_headers
    )

    assert get_response.status_code == 404

    # User 2 tries to UPDATE User 1's application
    update_response = client.put(
        f"/applications/{application_id}",
        json={
            "company": "Hacked Company",
            "role": "Hacked Role",
            "status": "Selected",
            "package": "50 LPA",
            "notes": "Unauthorized update"
        },
        headers=user2_headers
    )

    assert update_response.status_code == 404

    # User 2 tries to DELETE User 1's application
    delete_response = client.delete(
        f"/applications/{application_id}",
        headers=user2_headers
    )

    assert delete_response.status_code == 404

    # User 1 should still be able to access it
    owner_response = client.get(
        f"/applications/{application_id}",
        headers=user1_headers
    )

    assert owner_response.status_code == 200
    assert owner_response.json()["company"] == "Private Company"

    # Cleanup
    db = SessionLocal()

    application = db.query(Application).filter(
        Application.id == application_id
    ).first()

    if application:
        db.delete(application)

    user1 = db.query(User).filter(
        User.email == user1_email
    ).first()

    user2 = db.query(User).filter(
        User.email == user2_email
    ).first()

    if user1:
        db.delete(user1)

    if user2:
        db.delete(user2)

    db.commit()
    db.close()