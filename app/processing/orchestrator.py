from random import random

from app.domain.business_validation import validate_trailer
from app.domain.structural_validation import validate_structure
import app.persistence.job_repository as job_repository
from app.persistence.validation_error_repository import insert_validation_error
from app.processing import file_reader

def process_file(file_path: str) -> int:
    #print("process_file")
    job_id = job_repository.insert_job(file_path)

    job_repository.mark_job_as_processing(job_id)

    file_is_valid, error_message = validate_structure(file_path)

    if not run_structural_phase(file_path, job_id):
        return job_id

    file_reader.stream_file_lines(file_path, job_id)

    if not run_business_validation_phase(job_id):
        job_repository.finalize_job(job_id, 'PROCESSED_WITH_ERRORS')
    else:
        job_repository.finalize_job(job_id, 'PROCESSED')

    return job_id

    
def run_structural_phase(file_path, job_id) -> bool:
    file_is_valid, error_message = validate_structure(file_path)

    if not file_is_valid:
        job_repository.mark_job_as_rejected(job_id, 'REJECTED', error_message) 
        return False
    
    return True

def run_business_validation_phase(job_id):
    trailer_is_valid, trailer_row_id, error_message = validate_trailer(job_id)
    if not trailer_is_valid:
        insert_validation_error(job_id, 'BUSINESS_VALIDATION', error_message, trailer_row_id, 'BV001')
        return False
    return True