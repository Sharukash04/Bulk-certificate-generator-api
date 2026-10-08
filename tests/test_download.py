from fastapi.testclient import TestClient

from app.main import app
from app.database import SessionLocal
from app.models import Certificate

client=TestClient(app)


def test_certificate_failure():
    response=client.post(
        "/api/jobs/",
        json={
            "event_name":"Failure Test",
            "organization":"JJCET",
            "recipients":[
                {
                    "name":"Failure User",
                    "email":"failure@example.com"
                }
            ]
        }
    )

    assert response.status_code==200

    job_id=response.json()["job_id"]

    db=SessionLocal()

    certificate=db.query(Certificate).filter(
        Certificate.job_id==job_id
    ).first()

    certificate_id=certificate.id

    certificate.status="FAILED"
    certificate.error_message="Test generation failure"

    db.commit()
    db.close()

    response=client.get(
        f"/api/certificates/{certificate_id}"
    )

    assert response.status_code==400

    assert response.json()["detail"]=="Certificate is not available"


def test_certificate_not_found():
    response=client.get(
        "/api/certificates/999999"
    )

    assert response.status_code==404

    assert response.json()["detail"]=="Certificate not found"