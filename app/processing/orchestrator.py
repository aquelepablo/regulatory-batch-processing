from random import random

from app.domain.business_validation import validate_detail, validate_trailer
from app.domain.structural_validation import validate_structure
import app.persistence.job_repository as job_repository
from app.persistence.validation_error_repository import insert_validation_error
from app.processing import file_reader
from enum import Enum

class JobStatus(Enum):
    RECEIVED = "RECEIVED"
    PROCESSING = "PROCESSING"
    PROCESSED_WITH_ERRORS = "PROCESSED_WITH_ERRORS"
    PROCESSED = "PROCESSED"
    REJECTED = "REJECTED"


def process_file(file_path: str) -> int:
    #print("process_file")
    
    job_id = job_repository.insert_job(file_path, JobStatus.RECEIVED.value)
    
    job_repository.mark_job_as_processing(job_id, JobStatus.PROCESSING.value)

    error = validate_structure(file_path)
    if error:
        job_repository.mark_job_as_rejected(job_id, JobStatus.REJECTED.value, error)
        return job_id

    if not run_structural_phase(file_path, job_id):
        return job_id

    file_reader.stream_file_lines(file_path, job_id)

    if not run_business_validation_phase(job_id):
        return job_id
    
    job_repository.finalize_job(job_id, JobStatus.PROCESSED.value)

    return job_id

    
def run_structural_phase(file_path, job_id) -> bool:
    
    error_message = validate_structure(file_path)
    if error_message:
        job_repository.mark_job_as_rejected(job_id, JobStatus.REJECTED.value, error_message) 
        return False

    return True

def run_business_validation_phase(job_id) -> bool:
    #TODO: Validate Header

    trailer_is_invalid = validate_trailer(job_id)
    if trailer_is_invalid:
        trailer_row_id, error_code, error_message = trailer_is_invalid
        insert_validation_error(job_id, 'FILE_STRUCTURE', error_message, trailer_row_id, error_code)
        job_repository.mark_job_as_rejected(job_id, JobStatus.REJECTED.value, error_message) 
        return False
    
    errors = validate_detail(job_id)
    if errors > 0:
        job_repository.finalize_job_with_errors(job_id, JobStatus.PROCESSED_WITH_ERRORS.value, errors, 'Detail lines with inconsistences')
        return False
    
    return True

def get_job_status(job_id):
    
    job_status = job_repository.get_job_status(job_id)

    if job_status:
        return {
            "job_id": job_id,
            "status": job_status
        }

    return {
            "job_id": job_id,
            "status": "NOT_FOUND"
        }