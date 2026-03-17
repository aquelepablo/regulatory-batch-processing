# Regulatory Batch Processing System (V1)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791)
![SQL](https://img.shields.io/badge/SQL-Validation%20Engine-orange)
![Status](https://img.shields.io/badge/Status-Portfolio%20Demo-yellow)

A portfolio backend project that demonstrates how to design an auditable batch-processing workflow using **Python, FastAPI, PostgreSQL, and SQL-first validation**.

This project focuses on **clarity, lifecycle control, data traceability, and validation design** rather than production scale.

## Overview

The system receives a structured file through HTTP, validates its structure, persists raw records for traceability, executes business validations in SQL, and tracks the full job lifecycle.

Core ideas demonstrated in this repository:

- job-oriented batch processing
- explicit lifecycle transitions
- streaming ingestion
- raw data persistence for auditability
- SQL-first business validation
- separation between orchestration and validation logic

## Job Lifecycle

Each uploaded file is processed as a job with explicit status transitions:

```text
RECEIVED -> PROCESSING -> REJECTED | PROCESSED | PROCESSED_WITH_ERRORS
```

This keeps the workflow transparent and makes failures and processing outcomes easy to audit.

## What This Project Implements

- `POST /upload` endpoint to receive a file
- `GET /status/{job_id}` endpoint to inspect processing status
- file-level validation for header and trailer
- raw line persistence in PostgreSQL
- SQL-based validation for detail and trailer consistency
- final job status calculation
- unit and DB integration tests

## Architecture

Responsibilities are intentionally split between application and database layers.

### Python

- API surface
- orchestration
- file streaming
- lifecycle coordination
- transaction flow

### PostgreSQL + SQL

- raw data persistence
- set-based validations
- aggregation checks
- validation error storage

This design keeps Python focused on control flow while delegating validation-heavy logic to SQL.

For a deeper explanation, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Project Structure

```text
reg-batch-v1
├── app
│   ├── api
│   │   └── upload.py
│   ├── domain
│   │   ├── business_validation.py
│   │   └── structural_validation.py
│   ├── persistence
│   │   ├── db.py
│   │   ├── job_repository.py
│   │   ├── raw_record_repository.py
│   │   ├── validation_error_repository.py
│   │   └── sql
│   │       ├── validate_detail.sql
│   │       └── validate_trailer.sql
│   ├── processing
│   │   ├── file_reader.py
│   │   ├── job_lifecycle.py
│   │   └── orchestrator.py
│   └── main.py
├── docs
│   ├── tables.sql
│   ├── file_format.md
│   └── PAYMENTS_ACME_20250315_001.dat
├── tests
├── requirements.txt
└── README.md
```

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQL
- pytest
- python-dotenv
- psycopg2

## Running Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file based on `.env.example`.

### 3. Create the database schema

Run the SQL in:

```text
docs/tables.sql
```

### 4. Start the API

```bash
uvicorn app.main:app --reload
```

## Example Input

A sample batch file is available at:

```text
docs/PAYMENTS_ACME_20250315_001.dat
```

## Validation Strategy

The project separates validation into two categories.

### File-level validation

Executed before or during ingestion.

Examples:

- empty file
- invalid header
- invalid trailer

These errors are fatal and cause the job to be rejected.

### Record-level validation

Executed after persistence using SQL.

Examples:

- invalid detail fields
- numeric conversion issues
- trailer/detail consistency mismatches

These errors may either reject the job or finalize it as `PROCESSED_WITH_ERRORS`, depending on severity.

## Intentional V1 Constraints

This repository is intentionally scoped as a focused V1.

Not implemented:

- retries
- idempotency
- async/background processing
- parallel ingestion
- production-grade observability
- operational hardening

These trade-offs are intentional so the project stays centered on architecture, correctness, and auditability.

## Why This Project Matters

This repository was built to demonstrate backend engineering decisions commonly found in financial, regulatory, and enterprise batch systems:

- explicit workflow modeling
- audit-friendly persistence
- SQL-driven consistency checks
- clean separation of responsibilities
- predictable failure semantics

## License

This project is available for study, adaptation, and portfolio reference.
