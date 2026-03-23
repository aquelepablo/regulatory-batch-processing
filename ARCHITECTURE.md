# Architecture — Regulatory Batch Processing System (V1)

## Purpose

This document describes the core architectural decisions and processing flow of the **Regulatory Batch Processing System (V1)**.

The goal is not to present a production-ready system, but to clearly demonstrate how batch ingestion, validation, and lifecycle control can be designed in a **robust, auditable, and explicit way** using Python and SQL.

---

## High-Level Overview

The system processes each uploaded file as a **job** with a well-defined lifecycle.

Responsibilities are intentionally split:

- **Python**
  - orchestration
  - streaming file ingestion
  - lifecycle coordination
  - minimal HTTP API
- **Database (PostgreSQL)**
  - raw data persistence
  - set-based validations
  - aggregation and consistency checks
  - validation error recording

This separation keeps Python focused on control flow and clarity, while delegating heavy validation logic to SQL.

---

## Job Lifecycle

Each uploaded file follows a strict lifecycle:

```
RECEIVED -> PROCESSING -> REJECTED | PROCESSED | PROCESSED_WITH_ERRORS
```

### Lifecycle Semantics

- **RECEIVED**
  - File registered
  - No file content read yet
- **PROCESSING**
  - System assumes responsibility
  - File ingestion and validation start
- **REJECTED**
  - Fatal, file-level error
  - Processing stops immediately
- **PROCESSED**
  - File processed successfully
  - No validation errors
- **PROCESSED_WITH_ERRORS**
  - Non-fatal, record-level validation errors detected

---

## Validation Strategy

Validations are intentionally split into two categories.

### 1. File-Level (Fatal)

Executed before or during ingestion.

Examples:

- empty file
- invalid header
- invalid trailer

**Outcome:**  
Any failure immediately **rejects the job** and halts processing.

---

### 2. Record-Level (Fatal and Non-Fatal)

Executed after raw data persistence using SQL.

Examples:

- **Trailer inconsistencies - Fatal:**
  - trailer totals inconsistent with detail records

**Outcome:**  
Processing ends and the job is finalized as `REJECTED`.

- **Detail inconsistencies - Non-Fatal:**
  - invalid field formats
  - numeric conversion failures
  - business consistency rules

**Outcome:**  
Errors are recorded, but processing continues and the job is finalized as `PROCESSED_WITH_ERRORS`.

---

## Data Model (Conceptual)

- **processing_job**
  - one row per uploaded file
  - tracks lifecycle, timestamps, counters, and summary errors

- **raw_record**
  - immutable storage of each file line
  - preserves original content for auditability

- **validation_error**
  - records file-level and record-level issues
  - optionally linked to a specific raw record

Raw data is always persisted **exactly as received**.

---

## File Ingestion & Streaming

- Files are handled using **streaming I/O**
- Lines are processed incrementally
- Raw records are inserted using **batch inserts (`execute_values`)**
- The system avoids loading entire files into memory

Advanced ingestion techniques (e.g. `COPY`, parallelism, async pipelines) are intentionally deferred.

---

## Transaction & Consistency Model

- A **single database connection** is opened per job
- Auto-commit is disabled
- All writes for a job occur within an explicit transaction
- Any unexpected failure triggers a rollback
- A best-effort job rejection is attempted on fatal errors

This ensures:

- no partial ingestion
- consistent job state
- clear failure semantics

---

## Orchestration Flow (Simplified)

```
POST /upload
   ↓
create job (RECEIVED)
   ↓
mark PROCESSING
   ↓
structural validation
   ↓
stream file → persist raw records
   ↓
SQL business validations
   ↓
finalize job status
```

The orchestrator coordinates the workflow but does **not** implement heavy business rules.

---

## Intentional Constraints (V1)

This architecture prioritizes:

- correctness
- clarity
- auditability
- explicit lifecycle control

It does **not** prioritize:

- maximum throughput
- horizontal scalability
- async or distributed processing

These are conscious trade-offs for a focused V1.

---

## Expected Evolutions (V2+)

- richer validation catalogs
- normalized / parsed data tables
- COPY-based ingestion
- retries and idempotency
- background processing
- monitoring and metrics

---

## Final Note

This architecture reflects real-world batch processing patterns commonly found in regulatory, financial, and enterprise systems, intentionally simplified to highlight **design reasoning and lifecycle control** rather than operational scale.
