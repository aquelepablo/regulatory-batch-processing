# Regulatory Batch Processing System (V1) - Portfolio Demo

This is a portfolio V1 that demonstrates architecture, data integrity thinking, and backend workflow design.
It is not meant for production use or full operational readiness.

## Goal

Show that I can design a clear, auditable batch processing system that:

- receives a file via HTTP
- validates structure before persistence
- persists raw lines for traceability
- runs SQL-based business validations
- tracks job lifecycle and results

## Scope (V1)

In scope:

- streaming file ingestion (no full file in memory)
- raw data persistence for auditability
- SQL-first validation and aggregation
- job lifecycle tracking (RECEIVED -> PROCESSING -> PROCESSED/REJECTED)
- a minimal API surface

Out of scope:

- retries, idempotency, parallelism
- multiple file formats
- rich monitoring and alerts
- production hardening

## Design Highlights

- Job-oriented processing with explicit state transitions
- Early file-level rejection before persistence
- Raw line immutability to support audit and reprocessing
- SQL-first validation (set-based, not row-by-row Python)
- Simple orchestration layer, minimal business logic in code

## What Is Implemented

- API endpoints: `POST /upload`, `GET /status/{job_id}`
- File structure validation (header and trailer checks)
- Raw record persistence (batch insert with `execute_values`)
- Business validations in SQL (detail line checks, trailer totals)
- Job finalization and error reporting
- Unit and DB integration tests

## Known Limitations (Intentional for V1)

- Double file read: one pass for structural validation, one pass for persistence
- No retry/idempotency logic
- No async processing or queues
- Simplified error handling and logging

## How To Run (Optional)

This project is primarily for demonstration, but it can be run locally:

1. Create a virtualenv and install dependencies:
   `pip install -r requirements.txt`
2. Create a `.env` based on `.env.example`
3. Create DB schema: `docs/tables.sql`
4. Start the app:
   `uvicorn app.main:app --reload`

Use the sample file in `docs/PAYMENTS_ACME_20250315_001.dat`.
