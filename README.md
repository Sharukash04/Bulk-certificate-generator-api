# Bulk Certificate Generator API

A backend API for generating participation certificates in bulk from a predefined certificate template.

The API accepts multiple recipients in a single request, validates the recipient information, creates a generation job, generates individual PDF certificates in the background, tracks the progress and status of the job, handles individual certificate failures, and provides endpoints to retrieve generated certificates.

## Features

* Bulk certificate generation from a single API request
* Recipient name and email validation
* Predefined certificate template
* PDF certificate generation using ReportLab
* Background processing using FastAPI BackgroundTasks
* Generation job status tracking
* Completed and failed certificate counts
* Individual certificate status tracking
* Individual certificate failure handling
* Certificate PDF download
* Automated tests using Pytest
* SQLite database for job and certificate metadata

## Technology Stack

* **Python 3.14**
* **FastAPI** – REST API framework
* **SQLAlchemy** – ORM and database interaction
* **SQLite** – Relational database
* **Pydantic** – Request validation
* **ReportLab** – PDF certificate generation
* **Pytest** – Automated testing
* **Uvicorn** – ASGI server

## Project Structure

```text
bulk-certificate-generator-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── certificate_service.py
│   │   └── job_service.py
│   │
│   └── templates/
│
├── generated/
│
├── tests/
│   ├── __init__.py
│   ├── test_jobs.py
│   ├── test_validation.py
│   ├── test_generation.py
│   └── test_download.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Prerequisites

Make sure the following are installed:

* Python 3.14 or compatible Python 3.x version
* pip
* Git

## Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd bulk-certificate-generator-api
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Running the Application

Start the FastAPI development server using:

```powershell
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides interactive Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

The Swagger UI can be used to submit requests and test all API endpoints.

## API Endpoints

### 1. Create a Generation Job

**POST**

```text
/api/jobs/
```

This endpoint accepts multiple recipients in a single request.

Example request:

```json
{
  "event_name": "Python Workshop 2026",
  "organization": "JJCET",
  "recipients": [
    {
      "name": "Sharukash N",
      "email": "sharukash01@gmail.com"
    },
    {
      "name": "Test User",
      "email": "test@example.com"
    }
  ]
}
```

Example response:

```json
{
  "job_id": 3,
  "status": "PENDING",
  "total_recipients": 2
}
```

The API creates one generation job containing all recipients instead of requiring a separate request for every certificate.

---

### 2. Check Generation Job Status

**GET**

```text
/api/jobs/{job_id}
```

Example:

```text
/api/jobs/3
```

Example response:

```json
{
  "job_id": 3,
  "event_name": "Python Workshop 2026",
  "organization": "JJCET",
  "status": "COMPLETED",
  "total_recipients": 2,
  "completed": 2,
  "failed": 0
}
```

Possible job statuses include:

* `PENDING`
* `PROCESSING`
* `COMPLETED`
* `COMPLETED_WITH_ERRORS`

---

### 3. Get Certificates for a Job

**GET**

```text
/api/jobs/{job_id}/certificates
```

Example:

```text
/api/jobs/3/certificates
```

Example response:

```json
{
  "job_id": 3,
  "certificates": [
    {
      "certificate_id": 3,
      "recipient_name": "Sharukash N",
      "recipient_email": "sharukash01@gmail.com",
      "status": "SUCCESS",
      "file_path": "generated/certificate_3.pdf",
      "error_message": null
    },
    {
      "certificate_id": 4,
      "recipient_name": "Test User",
      "recipient_email": "test@example.com",
      "status": "SUCCESS",
      "file_path": "generated/certificate_4.pdf",
      "error_message": null
    }
  ]
}
```

This endpoint allows the client to see the status of each certificate individually.

---

### 4. Retrieve a Generated Certificate

**GET**

```text
/api/certificates/{certificate_id}
```

Example:

```text
/api/certificates/3
```

If the certificate was generated successfully, the API returns the PDF file for download.

Example response headers:

```text
Content-Type: application/pdf
Content-Disposition: attachment; filename="certificate_3.pdf"
```

If the certificate is not available, the API returns an appropriate error response.

## Validation

The API validates recipient data using Pydantic.

### Recipient name

* Required
* Minimum length: 2 characters
* Maximum length: 100 characters

### Recipient email

* Required
* Must be a valid email address

### Recipient list

* At least one recipient is required

Invalid input returns:

```text
HTTP 422 Unprocessable Entity
```

Example invalid request:

```json
{
  "event_name": "Validation Test",
  "organization": "JJCET",
  "recipients": [
    {
      "name": "A",
      "email": "invalid-email"
    }
  ]
}
```

## Certificate Generation

A single predefined certificate design is used for all recipients.

Each generated certificate contains:

* Certificate title
* Recipient name
* Event name
* Organization name
* Certificate ID

Certificates are generated as PDF files using ReportLab.

Generated files are stored in:

```text
generated/
```

## Background Processing

The application uses **FastAPI BackgroundTasks** for certificate generation.

The API first:

1. Validates the request.
2. Creates a generation job.
3. Creates certificate records for all recipients.
4. Returns the job ID.
5. Starts certificate generation in the background.

This allows the client to receive the job ID without waiting for every PDF to be generated.

### Why BackgroundTasks?

FastAPI BackgroundTasks was selected because this assignment is a lightweight backend application and does not require a distributed task queue.

It keeps the implementation simple while still demonstrating asynchronous-style job processing.

For a large-scale production system, a dedicated task queue such as Celery with Redis or RabbitMQ could be considered.

## Failure Handling

Each certificate is processed independently.

If certificate generation fails for one recipient:

* That certificate is marked as `FAILED`.
* The error message is stored.
* The job's failed count is increased.
* Processing continues for the remaining recipients.

After processing:

* If all certificates succeed, the job becomes `COMPLETED`.
* If one or more certificates fail, the job becomes `COMPLETED_WITH_ERRORS`.

This prevents a single certificate failure from unnecessarily stopping the entire bulk operation.

## Database Design

SQLite is used as the relational database.

### GenerationJob

Stores information about the bulk generation request.

Main fields:

* `id`
* `event_name`
* `organization`
* `total_recipients`
* `completed`
* `failed`
* `status`
* `created_at`

### Certificate

Stores information about each recipient's certificate.

Main fields:

* `id`
* `job_id`
* `recipient_name`
* `recipient_email`
* `status`
* `file_path`
* `error_message`

Relationship:

```text
GenerationJob
      │
      │ 1-to-many
      ▼
Certificate
```

One generation job can contain multiple certificates.

## Running Tests

Run the complete test suite using:

```powershell
python -m pytest
```

Current test result:

```text
8 passed
```

The test suite covers:

* Creating a generation job
* Retrieving job status
* Invalid email validation
* Invalid recipient name validation
* Empty recipient validation
* Certificate PDF generation
* Individual certificate failure handling
* Certificate not found handling

## Design Decisions

### 1. Bulk Request

The API accepts all recipients in one request.

This satisfies the bulk-processing requirement and avoids requiring one API request per certificate.

### 2. Background Processing

FastAPI BackgroundTasks is used instead of processing all certificates directly inside the request.

This allows the API to return a job ID quickly while certificate generation continues in the background.

### 3. Relational Database

SQLite with SQLAlchemy is used to store generation jobs and certificate metadata.

This provides persistent tracking of:

* Job status
* Certificate status
* Completion count
* Failure count
* Generated file locations
* Error messages

### 4. Predefined Template

The application uses one fixed certificate template generated using ReportLab.

A certificate editor or multiple templates are intentionally not included because the assignment requires one predefined template.

### 5. Individual Failure Handling

Certificate generation is performed inside an individual `try/except` block.

Therefore, a failure while generating one certificate does not stop the remaining certificates.

## Example Workflow

```text
Client
  │
  │ POST /api/jobs/
  ▼
FastAPI
  │
  ├── Validate recipients
  │
  ├── Create GenerationJob
  │
  ├── Create Certificate records
  │
  └── Start BackgroundTask
          │
          ▼
   Generate certificates
          │
          ├── SUCCESS
          │
          └── FAILED
          │
          ▼
       Update DB
          │
          ▼
Client checks:
GET /api/jobs/{job_id}
          │
          ▼
GET /api/jobs/{job_id}/certificates
          │
          ▼
GET /api/certificates/{certificate_id}
```

## Future Improvements

Possible improvements for a production-scale version include:

* Celery + Redis/RabbitMQ for distributed background processing
* PostgreSQL instead of SQLite
* Cloud object storage such as AWS S3
* Authentication and authorization
* Rate limiting
* Unique job identifiers such as UUIDs
* Certificate expiration or cleanup policies
* Email delivery of generated certificates
* Batch pagination for very large recipient lists
* Structured application logging
* Docker containerization
* CI/CD pipeline with GitHub Actions

## Assignment Scope

This project implements the **Bulk Certificate Generator API** assignment.

The implementation focuses on:

* Bulk request handling
* Input validation
* PDF certificate generation
* Background processing
* Job progress tracking
* Individual failure handling
* Certificate retrieval
* Automated testing

The application uses a single predefined certificate template and does not include certificate template editing or multiple design support.
