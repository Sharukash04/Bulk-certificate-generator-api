from fastapi.testclient import TestClient

from app.main import app

client=TestClient(app)


def test_invalid_email():
    response=client.post(
        "/api/jobs/",
        json={
            "event_name":"Validation Test",
            "organization":"JJCET",
            "recipients":[
                {
                    "name":"Test User",
                    "email":"invalid-email"
                }
            ]
        }
    )

    assert response.status_code==422


def test_invalid_name():
    response=client.post(
        "/api/jobs/",
        json={
            "event_name":"Validation Test",
            "organization":"JJCET",
            "recipients":[
                {
                    "name":"A",
                    "email":"test@example.com"
                }
            ]
        }
    )

    assert response.status_code==422


def test_empty_recipients():
    response=client.post(
        "/api/jobs/",
        json={
            "event_name":"Validation Test",
            "organization":"JJCET",
            "recipients":[]
        }
    )

    assert response.status_code==422