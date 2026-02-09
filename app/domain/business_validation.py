from app.persistence.db import get_connection
from app.processing.file_reader import load_sql
import psycopg2

trailer_queries = 'validate_trailer.sql'

def validate_trailer(job_id: int) -> tuple[int, str, str] | None:
    sql = load_sql(trailer_queries)
    params = {"job_id": job_id}

    try:
        conn = get_connection()

        with conn:
            with conn.cursor() as curs:
                curs.execute(sql, params)
                row =  curs.fetchone()

        if not row:
            return None

        trailer_row_id, error_code, error_message = row

        return trailer_row_id, error_code, error_message

    except (psycopg2.DatabaseError) as e:
        full_sql = curs.mogrify(sql, params).decode("utf-8")
        raise RuntimeError(
            f"Database error while inserting job: {e}\n"
            f"Query: {full_sql}"
        )
    except (Exception) as e:
        raise RuntimeError(f"Database error while inserting job: {e}")