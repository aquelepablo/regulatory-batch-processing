import psycopg2

def insert_validation_error(conn, job_id: int, error_type: str, error_message: str, raw_record_id: int | None = None, error_code: str | None = None) -> None:
    cursor = conn.cursor()
    sql = """
        INSERT INTO validation_error(job_id, raw_record_id, error_type, error_code, error_message) 
        VALUES(%(job_id)s, %(raw_record_id)s, %(error_type)s, %(error_code)s, %(error_message)s)
    """
                
    params = {
        "job_id": job_id,
        "raw_record_id": raw_record_id, 
        "error_type": error_type, 
        "error_code": error_code, 
        "error_message": error_message
    }

    try:
        cursor.execute(sql, params)

    except (psycopg2.DatabaseError) as e:
        raise RuntimeError(
            f"""
            Database error while inserting validation_error 
            job_id={job_id}
            raw_record_id={raw_record_id}
            raw_record_id={raw_record_id}
            error_type={error_type}
            error_code={error_code}
            error_message={error_message}
            error={e}
            """
        )

