import psycopg2


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

