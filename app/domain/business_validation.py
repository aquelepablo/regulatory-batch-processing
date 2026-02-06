from app.processing.file_reader import load_sql
import psycopg2

trailer_queries = 'validate_trailer.sql'

def validate_trailer(job_id: int) -> tuple[bool, int | None, str | None]:
    sql = load_sql(trailer_queries)
    params = {"job_id": job_id}

    try:
        conn = psycopg2.connect(
            dbname="regulatory_batch",
            user="postgres",
            password="1234",
            host="localhost"
        )

        with conn:
            with conn.cursor() as curs:
                curs.execute(sql, params)
                trailer_is_valid, trailer_row_id =  curs.fetchone()

        return trailer_is_valid, trailer_row_id, error_message

    except (psycopg2.DatabaseError) as e:
        full_sql = curs.mogrify(sql, params).decode("utf-8")
        raise RuntimeError(
            f"Database error while inserting job: {e}\n"
            f"Query: {full_sql}"
        )
    except (Exception) as e:
        raise RuntimeError(f"Database error while inserting job: {e}")