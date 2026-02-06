import psycopg2

def insert_validation_error(job_id: int, error_type: str, error_message: str, raw_record_id: int | None = None, error_code: str | None = None) -> None:
    print('insert_validation_error')

    try:
        conn = psycopg2.connect(
            dbname="regulatory_batch",
            user="postgres",
            password="1234",
            host="localhost"
        )

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


    pass


#INSERT INTO validation_error(job_id, raw_record_id, error_type, error_code, error_message) VALUES(v_job_id, v_raw_record_id, 'BUSINESS_VALIDATION', 'B01', 'INCORRECT DATA');

def insert_raw_record(job_id: int, line_number: int, raw_content: str, parsed_ok: bool):
    print("insert_raw_record")
    
    try:
        conn = psycopg2.connect(
            dbname="regulatory_batch",
            user="postgres",
            password="1234",
            host="localhost"
        )

        with conn:
            with conn.cursor() as curs:
                
                sql = """
                      INSERT INTO raw_record(job_id, line_number, raw_content, parsed_ok) 
                      VALUES(%s, %s, %s, %s)
                      """
                params = (job_id, line_number, raw_content, parsed_ok)

                curs.execute(sql, params)

            # a more robust way of handling errors

    except (psycopg2.DatabaseError) as e:
        full_sql = curs.mogrify(sql, params).decode("utf-8")
        raise RuntimeError(
            f"Database error while inserting job: {e}\n"
            f"Query: {full_sql}"
        )
    except (Exception) as e:
        raise RuntimeError(f"Database error while inserting job: {e}")

