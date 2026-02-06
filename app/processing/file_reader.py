from app.persistence.raw_record_repository import insert_raw_record


def stream_file_lines(file_path: str, job_id: int):
    print('stream_file_lines')

    line_parsed = False #No parse line for now

    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, 1):
            insert_raw_record(job_id, line_number, line.strip(), line_parsed)

#TODO: Returns 'HEADER' | 'DETAIL' | 'TRAILER'
def classify_line(line: str):
    pass

