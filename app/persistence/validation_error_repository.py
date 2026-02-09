import psycopg2

from app.persistence.db import get_connection

def insert_validation_error(job_id: int, error_type: str, error_message: str, raw_record_id: int | None = None, error_code: str | None = None) -> None:
    print('insert_validation_error')

    try:
        conn = get_connection()

        with conn:
            with conn.cursor() as curs:
                
                sql = """
                      INSERT INTO validation_error(job_id, raw_record_id, error_type, error_code, error_message) 
                      VALUES(%(job_id)s, %(raw_record_id)s, %(error_type)s, %(error_code)s, %(error_message)s)
                      """
                
                params = {"job_id": job_id,
                          "raw_record_id": raw_record_id, 
                          "error_type": error_type, 
                          "error_code": error_code, 
                          "error_message": error_message}

                curs.execute(sql, params)

    except (psycopg2.DatabaseError) as e:
        full_sql = curs.mogrify(sql, params).decode("utf-8")
        raise RuntimeError(
            f"Database error while inserting job: {e}\n"
            f"Query: {full_sql}"
        )
    except (Exception) as e:
        raise RuntimeError(f"Database error while inserting job: {e}")

