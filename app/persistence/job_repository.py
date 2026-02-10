import psycopg2

#TODO: FIX USER ON DB CONNECTION
def insert_job(conn, file_name, job_status) -> int:
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO processing_job(file_name, received_at, status) 
            VALUES(%s, NOW(), %s) 
            RETURNING job_id
            """,
            (file_name, job_status)
        )

        job_id = cursor.fetchone()[0]

        return job_id

    except (psycopg2.DatabaseError) as e:
        raise RuntimeError(
            f"""
            Database error while inserting processing_job 
            file_name={file_name}
            error={e}
            """
        )

def mark_job_as_processing(conn, job_id, job_status) -> None:
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE processing_job
            SET started_at = NOW(),
                status = %s
            WHERE job_id = %s
            """,
            (job_status, job_id,)
        )

        if cursor.rowcount == 0:
            raise ValueError(f"Job {job_id} not found")

    except (psycopg2.DatabaseError) as e:
        raise RuntimeError(
            f"""
            Database error while updating processing_job 
            job_id={job_id}
            job_status={job_status}
            error={e}
            """
        )
    

def mark_job_as_rejected(conn, job_id, final_status, error_message) -> None:
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE processing_job
            SET finished_at = NOW(),
                status = %s,
                general_error_message = %s
            WHERE job_id = %s
            """,
            (final_status, error_message, job_id,)
        )

        if cursor.rowcount == 0:
            raise ValueError(f"Job {job_id} not found")

    except (psycopg2.DatabaseError) as e:
        raise RuntimeError(
            f"""
            Database error while updating processing_job 
            job_id={job_id}
            job_status={final_status}
            error_message={error_message}
            error={e}
            """
        )

def update_job_counters(conn, job_id, total_records, total_errors) -> None:
    pass

def finalize_job_with_errors(conn, job_id, final_status, total_errors, error_message) -> None:
    cursor = conn.cursor()
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

    try:
        cursor.execute(sql, params)

        if cursor.rowcount == 0:
            raise ValueError(f"Job {job_id} not found")

    except (psycopg2.DatabaseError) as e:
        raise RuntimeError(
            f"""
            Database error while updating processing_job 
            job_id={job_id}
            job_status={final_status}
            error_message={error_message}
            error={e}
            """
    )

def finalize_job(conn, job_id, final_status) -> None:
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """
            UPDATE processing_job
            SET finished_at = NOW(),
                status = %s
            WHERE job_id = %s
            """, 
            (final_status, job_id,)
        )

        if cursor.rowcount == 0:
            raise ValueError(f"Job {job_id} not found")

    except (psycopg2.DatabaseError) as e:
        raise RuntimeError(
            f"""
            Database error while updating processing_job 
            job_id={job_id}
            job_status={final_status}
            error={e}
            """
    )

def get_job_error_count(conn, job_id) -> int:
    pass

def get_job_status(conn, job_id) -> str | None:
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COALESCE(status, NULL) 
            FROM processing_job
            WHERE job_id = %s
            """,
            (job_id,)
        )

        if cursor.rowcount > 0:
            row = cursor.fetchone()[0]
            return row

        return None

    except (psycopg2.DatabaseError) as e:
        raise RuntimeError(
            f"""
            Database error while SELECT processing_job 
            job_id={job_id}
            error={e}
            """
    )


