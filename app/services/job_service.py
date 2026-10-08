from app.database import SessionLocal
from app.models import GenerationJob,Certificate
from app.services.certificate_service import generate_certificate


def process_generation_job(job_id:int):
    db=SessionLocal()

    try:
        job=db.query(GenerationJob).filter(
            GenerationJob.id==job_id
        ).first()

        if job is None:
            return

        job.status="PROCESSING"
        db.commit()

        certificates=db.query(Certificate).filter(
            Certificate.job_id==job_id
        ).all()

        for certificate in certificates:
            try:
                certificate.status="PROCESSING"
                db.commit()

                file_path=generate_certificate(
                    recipient_name=str(certificate.recipient_name),
                    event_name=str(job.event_name),
                    organization=str(job.organization),
                    certificate_id=int(certificate.id)
                )

                certificate.file_path=file_path
                certificate.status="SUCCESS"

                job.completed=int(job.completed)+1
                db.commit()

            except Exception as error:
                certificate.status="FAILED"
                certificate.error_message=str(error)

                job.failed=int(job.failed)+1
                db.commit()

        if int(job.failed)>0:
            job.status="COMPLETED_WITH_ERRORS"
        else:
            job.status="COMPLETED"

        db.commit()

    finally:
        db.close()