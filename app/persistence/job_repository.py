"""
Docstring for app.persistence.job_repository
insert_job
update_job_status
update_job_counters
get_job_error_count
"""

from os import error
from sqlite3 import DatabaseError
import psycopg2

from app.persistence.db import get_connection

#TODO: FIX USER ON DB CONNECTION
def insert_job(file_name, job_status) -> int:
    print("insert_job")
    
    try:

        conn = get_connection()

        with conn:
            with conn.cursor() as curs:
                
                curs.execute(
                    """
                    INSERT INTO processing_job(file_name, received_at, status) 
                    VALUES(%s, NOW(), %s) 
                    RETURNING job_id
                    """,
                    (file_name, job_status)
                )

                job_id = curs.fetchone()[0]

                return job_id

            # a more robust way of handling errors
    except (Exception, psycopg2.DatabaseError) as e:
        raise RuntimeError(f"Database error while inserting job: {e}")


def mark_job_as_processing(job_id, job_status) -> None:
    print("mark_job_as_processing")

    try:
        conn = get_connection()

        with conn:
            with conn.cursor() as curs:
                
                curs.execute(
                    """
                    UPDATE processing_job
                    SET started_at = NOW(),
                        status = %s
                    WHERE job_id = %s
                    """,
                    (job_status, job_id,)
                )

                if curs.rowcount == 0:
                    raise ValueError(f"Job {job_id} not found")

            # a more robust way of handling errors
    except (Exception, psycopg2.DatabaseError) as e:
        raise RuntimeError(f"Database error while updating job {job_id}: {e}")


def mark_job_as_rejected(job_id, final_status, error_message) -> None:
    print("mark_job_as_rejected")
    try:
        conn = get_connection()

        with conn:
            with conn.cursor() as curs:
                
                curs.execute(
                    """
                    UPDATE processing_job
                    SET finished_at = NOW(),
                        status = %s,
                        general_error_message = %s
                    WHERE job_id = %s
                    """,
                    (final_status, error_message, job_id,)
                )

                if curs.rowcount == 0:
                    raise ValueError(f"Job {job_id} not found")

            # a more robust way of handling errors
    except (Exception, psycopg2.DatabaseError) as e:
        raise RuntimeError(f"Database error while updating job {job_id}: {e}")

def update_job_counters(conn, job_id, total_records, total_errors) -> None:
    pass

def finalize_job_with_errors(job_id, final_status, total_errors, error_message) -> None:
    print("finalize_job_with_errors")
    try:
        conn = get_connection()

        with conn:
            with conn.cursor() as curs:

                sql =   """
                        UPDATE processing_job
                        SET finished_at = NOW(),
                            status = %(status)s,
                            total_errors = %(total_errors)s,
                            general_error_message = %(error_message)s
                        WHERE job_id = %(job_id)s
                        """
                params = {
                            "status": final_status,
                            "total_errors": total_errors,
                            "error_message": error_message,
                            "job_id": job_id
                        }
                curs.execute(sql, params)

                if curs.rowcount == 0:
                    raise ValueError(f"Job {job_id} not found")

    except (psycopg2.DatabaseError) as e:
        full_sql = curs.mogrify(sql, params).decode("utf-8")
        raise RuntimeError(
            f"Database error while updating job {job_id}: {e}\n"
            f"Query: {full_sql}"
        )
    except (Exception) as e:
        raise RuntimeError(f"Database error while updating job {job_id}: {e}")



def finalize_job(job_id, final_status) -> None:
    print("finalize_job")
    try:

        conn = get_connection()

        with conn:
            with conn.cursor() as curs:
                
                sql = """
                    UPDATE processing_job
                    SET finished_at = NOW(),
                        status = %s
                    WHERE job_id = %s
                    """
                params = (final_status, job_id,)

                curs.execute(sql, params)

                if curs.rowcount == 0:
                    raise ValueError(f"Job {job_id} not found")

    except (psycopg2.DatabaseError) as e:
        full_sql = curs.mogrify(sql, params).decode("utf-8")
        raise RuntimeError(
            f"Database error while updating job {job_id}: {e}\n"
            f"Query: {full_sql}"
        )
    except (Exception) as e:
        raise RuntimeError(f"Database error while updating job {job_id}: {e}")

def get_job_error_count(conn, job_id) -> int:
    pass

def get_job_status(job_id) -> str | None:
    print("get_job_status")
    try:
        conn = get_connection()

        with conn:
            with conn.cursor() as curs:
                
                curs.execute(
                    """
                    SELECT status FROM processing_job
                    WHERE job_id = %s
                    """,
                    (job_id,)
                )

                row = curs.fetchone()[0]

                if not row:
                    return None
                
                return row

            # a more robust way of handling errors
    except (Exception, psycopg2.DatabaseError) as e:
        raise RuntimeError(f"Database error while geting job {job_id} status: {e}")


