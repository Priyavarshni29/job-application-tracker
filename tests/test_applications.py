from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Job Application Tracker API is running"


def test_create_application():
    data = {
        "company": "Test Company",
        "role": "Software Engineer",
        "status": "Applied",
        "package": "8 LPA",
        "notes": "Automated test application"
    }

    response = client.post("/applications/", json=data)

    assert response.status_code == 200

    result = response.json()

    assert result["company"] == "Test Company"
    assert result["role"] == "Software Engineer"
    assert result["status"] == "Applied"

    global test_application_id
    test_application_id = result["id"]


def test_get_application():
    response = client.get(f"/applications/{test_application_id}")

    assert response.status_code == 200

    result = response.json()

    assert result["id"] == test_application_id
    assert result["company"] == "Test Company"


def test_update_application():
    data = {
        "company": "Test Company",
        "role": "Backend Developer",
        "status": "Interview",
        "package": "10 LPA",
        "notes": "Updated by automated test"
    }

    response = client.put(
        f"/applications/{test_application_id}",
        json=data
    )

    assert response.status_code == 200

    result = response.json()

    assert result["role"] == "Backend Developer"
    assert result["status"] == "Interview"


def test_delete_application():
    response = client.delete(
        f"/applications/{test_application_id}"
    )

    assert response.status_code == 200

    assert response.json()["message"] == "Application deleted successfully"


def test_deleted_application_not_found():
    response = client.get(
        f"/applications/{test_application_id}"
    )

    assert response.status_code == 404