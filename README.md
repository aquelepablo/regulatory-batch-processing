# Regulatory Batch Processing System (V1)

## Project Overview

This project demonstrates a simplified batch processing system for ingesting and processing regulatory data files, emphasizing streaming ingestion, SQL-based validation, and an auditable, production-oriented design focused on data integrity.

## Folder Structure:

<pre>
reg-batch-v1/
│
├── app/
│ ├── api/ # System entry points (FastAPI endpoints)
│ ├── processing/ # Batch orchestration and file streaming/parsing
│ ├── persistence/ # Database access and SQL-based operations
│ ├── domain/ # Business rules and validation logic
│ └── main.py # Application bootstrap
│
├── docs/ # Sample files and documentation
│
├── README.md
└── .gitignore
</pre>

## Problem Statement

Many regulatory and enterprise systems still rely on large batch files to exchange and process critical data.
Unreliable validations or memory-dependent processing of sensitive, critical files may lead to data inconsistencies,
financial losses, or even regulatory risks.
In this kind of processing, small errors — such as a misplaced character — are often hard to detect, difficult to trace,
and can cause significant downstream issues.

## Scope (V1)

### In Scope

1. Process large files using streaming (no full file in memory)
2. Persist raw data for traceability and audit
3. Execute SQL-based validations and aggregations
4. Receive batch files via a minimal HTTP API
5. Track processing status per job
6. Generate a basic processing summary

### Out of Scope

- Support for multiple file formats
- Retry and idempotent processing
- Richer audit and processing details
- Advanced operational concerns
- Extended API and monitoring capabilities

## High-Level Architecture

The system is designed around a controlled, job-oriented batch processing flow, where each file is handled as an explicit processing job with a well-defined lifecycle.

Files are received through a minimal HTTP API and registered as processing jobs. Python is responsible for orchestrating the ingestion phase, performing streaming-based file reading and enforcing initial structural validations to ensure the file matches the expected layout before any business processing occurs.

Raw data is persisted early in the process to guarantee traceability and auditability. Once structural validation succeeds, Python delegates business validations and aggregations to the database, favoring set-based SQL operations over row-by-row processing for consistency and performance.

Validation results are recorded at both record and job levels. Python consolidates these outcomes to determine the final processing state, enabling detailed error analysis and a clear, auditable result for each processed file.

The architecture intentionally prioritizes data integrity, auditability and clarity over architectural complexity or real-time processing concerns.

The validation process is intentionally split into file-level (fatal) and record-level (non-fatal) validations.
File-level inconsistencies (e.g. header/trailer mismatches) cause the entire job to be rejected, while record-level errors are accumulated and reported without interrupting processing.

## Key Design Decisions

- **Job-oriented processing model**: each file is treated as an explicit processing job with a well-defined lifecycle and status transitions.
- **Raw data immutability**: all file lines (header, detail, trailer) are persisted exactly as received to support auditability and reprocessing.
- **SQL-first business validation**: data consistency and business rules are validated using set-based SQL operations, avoiding row-by-row processing in Python.
- **Early rejection for file-level errors**: structural and file consistency errors immediately reject the job, preventing unnecessary downstream processing.
- **Minimal orchestration layer**: Python coordinates the workflow and lifecycle but does not implement heavy business logic.

## Natural Evolutions (V2+)

- Introduce record-level business validations (e.g. amount format, account checksum).
- Externalize validation error codes and messages.
- Support multiple file formats.
- Add retry and idempotency controls.
- Persist parsed/normalized records for downstream processing.
- Improve operational metrics and monitoring.

## How to Run (Local)
