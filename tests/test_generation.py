import os

from app.services.certificate_service import generate_certificate


def test_certificate_generation():
    file_path=generate_certificate(
        recipient_name="Test User",
        event_name="Python Workshop",
        organization="JJCET",
        certificate_id=9999
    )

    assert file_path is not None
    assert os.path.exists(file_path)
    assert file_path.endswith(".pdf")

    os.remove(file_path)