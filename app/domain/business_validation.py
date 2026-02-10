from app.processing.file_reader import load_sql
import psycopg2



def validate_trailer(conn, job_id: int) -> tuple[int, str, str] | None:
    
    cursor = conn.cursor()

    sql = load_sql('validate_trailer.sql')
    params = {"job_id": job_id}

    try:
        cursor.execute(sql, params)
        row =  cursor.fetchone()

        if not row:
            return None

        trailer_row_id, error_code, error_message = row

        return trailer_row_id, error_code, error_message

    except (psycopg2.DatabaseError) as e:
        raise RuntimeError(
            f"""
            Database error while validating trailer 
            job_id={job_id}
            error={e}
            """
        )


def validate_detail(conn, job_id: int) -> int:
    
    cursor = conn.cursor()
    
    sql = load_sql('validate_detail.sql')
    params = {"job_id": job_id}

    try:
        cursor.execute(sql, params)
        row =  cursor.fetchone()[0]

        return row

    except (psycopg2.DatabaseError) as e:
        raise RuntimeError(
            f"""
            Database error while validating detail lines 
            job_id={job_id}
            error={e}
            """
        )