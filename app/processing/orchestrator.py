from random import random

from app.domain.structural_validation import validate_structure
import app.persistence.job_repository as job_repository
from app.processing import file_reader

def process_file(file_path: str) -> int:
    print("process_file")
    job_id = job_repository.insert_job(file_path)

    job_repository.mark_job_as_processing(job_id)

    file_is_valid, error_message = validate_structure(file_path)

    if file_is_valid:
        file_reader.stream_file_lines(file_path, job_id)

        job_repository.finalize_job(job_id, 'PROCESSED')
    else:
       job_repository.mark_job_as_rejected(job_id, 'REJECTED', error_message) 

    return job_id

    
