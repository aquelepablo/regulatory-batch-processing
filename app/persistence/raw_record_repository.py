from sqlite3 import Cursor
import psycopg2
import psycopg2.extras
from app.persistence.db import get_connection

def insert_raw_record(conn, job_id: int, line_number: int, raw_content: str, parsed_ok: bool):
    print("insert_raw_record")
    
    cursor = conn.cursor()

    sql = """
            INSERT INTO raw_record(job_id, line_number, raw_content, parsed_ok) 
            VALUES(%s, %s, %s, %s)
        """
    params = (job_id, line_number, raw_content, parsed_ok) 

    try:
        cursor.execute(sql, params)

    except (psycopg2.DatabaseError) as e:
        raise RuntimeError(
            f"""
            Database error while inserting raw_record 
            job_id={job_id}
            line_number={line_number}
            error={e}
            """
        )

def persist_raw_records_batch(conn, records):
    print("persist_raw_records_batch")
    
    cursor = conn.cursor()

    try:
        psycopg2.extras.execute_values(
            cursor, 
            """
            INSERT INTO raw_record(job_id, line_number, raw_content) 
            VALUES %s
            """, 
            records)

    except psycopg2.DatabaseError as e:
        raise RuntimeError(
            f"""
            Batch insert failed
            batch_size={len(records)}
            first_record={records[0] if records else None}
            error={e}
            """
        )

    finally:
        cursor.close()