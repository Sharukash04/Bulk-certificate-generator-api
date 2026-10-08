from fastapi import APIRouter,Depends,BackgroundTasks,HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import GenerationJob,Certificate
from app.schemas import GenerationRequest
from app.services.job_service import process_generation_job

router=APIRouter()


@router.post("/jobs/")
def create_generation_job(
    request:GenerationRequest,
    background_tasks:BackgroundTasks,
    db:Session=Depends(get_db)
):
    job=GenerationJob(
        event_name=request.event_name,
        organization=request.organization,
        total_recipients=len(request.recipients),
        status="PENDING"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    for recipient in request.recipients:
        certificate=Certificate(
            job_id=job.id,
            recipient_name=recipient.name,
            recipient_email=recipient.email,
            status="PENDING"
        )

        db.add(certificate)

    db.commit()

    background_tasks.add_task(
        process_generation_job,
        job.id
    )

    return {
        "job_id":job.id,
        "status":job.status,
        "total_recipients":job.total_recipients
    }


@router.get("/jobs/{job_id}")
def get_generation_job(
    job_id:int,
    db:Session=Depends(get_db)
):
    job=db.query(GenerationJob).filter(
        GenerationJob.id==job_id
    ).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return {
        "job_id":job.id,
        "event_name":job.event_name,
        "organization":job.organization,
        "status":job.status,
        "total_recipients":job.total_recipients,
        "completed":job.completed,
        "failed":job.failed
    }


@router.get("/jobs/{job_id}/certificates")
def get_job_certificates(
    job_id:int,
    db:Session=Depends(get_db)
):
    job=db.query(GenerationJob).filter(
        GenerationJob.id==job_id
    ).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    certificates=db.query(Certificate).filter(
        Certificate.job_id==job_id
    ).all()

    return {
        "job_id":job_id,
        "certificates":[
            {
                "certificate_id":certificate.id,
                "recipient_name":certificate.recipient_name,
                "recipient_email":certificate.recipient_email,
                "status":certificate.status,
                "file_path":certificate.file_path,
                "error_message":certificate.error_message
            }
            for certificate in certificates
        ]
    }


@router.get("/certificates/{certificate_id}")
def get_certificate(
    certificate_id:int,
    db:Session=Depends(get_db)
):
    certificate=db.query(Certificate).filter(
        Certificate.id==certificate_id
    ).first()

    if certificate is None:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    if certificate.status!="SUCCESS":
        raise HTTPException(
            status_code=400,
            detail="Certificate is not available"
        )

    if certificate.file_path is None:
        raise HTTPException(
            status_code=404,
            detail="Certificate file not found"
        )

    return FileResponse(
        path=certificate.file_path,
        media_type="application/pdf",
        filename=f"certificate_{certificate.id}.pdf"
    )