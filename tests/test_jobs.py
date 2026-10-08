from fastapi.testclient import TestClient

from app.main import app

client=TestClient(app)


def test_create_generation_job():
    response=client.post(
        "/api/jobs/",
        json={
            "event_name":"Test Workshop",
            "organization":"JJCET",
            "recipients":[
                {
                    "name":"Test User",
                    "email":"test@example.com"
                },
                {
                    "name":"Another User",
                    "email":"another@example.com"
                }
            ]
        }
    )

    assert response.status_code==200

    data=response.json()

    assert "job_id" in data
    assert data["status"]=="PENDING"
    assert data["total_recipients"]==2


def test_get_generation_job():
    response=client.post(
        "/api/jobs/",
        json={
            "event_name":"Status Test",
            "organization":"JJCET",
            "recipients":[
                {
                    "name":"Status User",
                    "email":"status@example.com"
                }
            ]
        }
    )

    assert response.status_code==200

    job_id=response.json()["job_id"]

    response=client.get(
        f"/api/jobs/{job_id}"
    )

    assert response.status_code==200

    data=response.json()

    assert data["job_id"]==job_id
    assert data["total_recipients"]==1
    assert "status" in data
    assert "completed" in data
    assert "failed" in data