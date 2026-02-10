"""
One-time local setup (run manually, not by pytest)

1) Create a dedicated test database (recommended):
   # in psql
   CREATE DATABASE reg_batch_test;

2) Export env vars before running pytest (PowerShell):
   $env:TEST_DB_NAME="reg_batch_test"
   $env:TEST_DB_USER="postgres"
   $env:TEST_DB_PASSWORD="1234"
   $env:TEST_DB_HOST="localhost"
   $env:TEST_DB_PORT="5432"

3) Run the integration test:
   $env:PYTHONPATH="$PWD"; pytest -q -v tests/test_process_file_happy_path.py
"""


import os
from pathlib import Path

import psycopg2
import pytest

from app.processing.orchestrator import process_file


def connect_test_db():
    return psycopg2.connect(
        dbname=os.environ["TEST_DB_NAME"],
        user=os.environ["TEST_DB_USER"],
        password=os.environ["TEST_DB_PASSWORD"],
        host=os.environ.get("TEST_DB_HOST", "localhost"),
        port=os.environ.get("TEST_DB_PORT", "5432"),
    )


@pytest.fixture(scope="session", autouse=True)
def setup_schema():
    schema_path = Path(__file__).resolve().parents[1] / "tests" / "sql" / "schema.sql"
    with connect_test_db() as conn, conn.cursor() as cur:
        cur.execute(schema_path.read_text(encoding="utf-8"))


@pytest.fixture(autouse=True)
def clean_tables():
    with connect_test_db() as conn, conn.cursor() as cur:
        cur.execute(
            "TRUNCATE validation_error, raw_record, processing_job RESTART IDENTITY CASCADE;"
        )


def test_process_file_happy_path(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_NAME", os.environ["TEST_DB_NAME"])
    monkeypatch.setenv("DB_USER", os.environ["TEST_DB_USER"])
    monkeypatch.setenv("DB_PASSWORD", os.environ["TEST_DB_PASSWORD"])
    monkeypatch.setenv("DB_HOST", os.environ.get("TEST_DB_HOST", "localhost"))
    monkeypatch.setenv("DB_PORT", os.environ.get("TEST_DB_PORT", "5432"))

    header = "H" + ("0" * 29)
    d1 = "D" + "1234567890" + "000000000100" + "0000001"
    d2 = "D" + "1234567891" + "000000000200" + "0000002"
    trailer = "T" + "00000002" + "00000000000300" + "0000004"

    p = tmp_path / "ok.dat"
    p.write_text("\n".join([header, d1, d2, trailer]) + "\n", encoding="utf-8")

    job_id = process_file(str(p))

    with connect_test_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT status, total_errors FROM processing_job WHERE job_id=%s", (job_id,))
        status, total_errors = cur.fetchone()
        assert status == "PROCESSED"
        assert total_errors == 0

        cur.execute("SELECT COUNT(*) FROM raw_record WHERE job_id=%s", (job_id,))
        assert cur.fetchone()[0] == 4

        cur.execute("SELECT COUNT(*) FROM validation_error WHERE job_id=%s", (job_id,))
        assert cur.fetchone()[0] == 0
