from random import random

from app.domain.business_validation import validate_detail, validate_trailer
from app.domain.structural_validation import validate_structure
from app.persistence.db import get_connection
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

    conn = get_connection()
    job_id = None

    try:
        conn.autocommit = False

        job_id = job_repository.insert_job(conn, file_path, JobStatus.RECEIVED.value)
        
        job_repository.mark_job_as_processing(conn, job_id, JobStatus.PROCESSING.value)

        # Structural validation (file-level, before DB load)
        error = validate_structure(file_path)
        if error:
            job_repository.mark_job_as_rejected(conn, job_id, JobStatus.REJECTED.value, error)
            conn.commit()
            return job_id

        # Persist raw records (batch, transactional)
        file_reader.stream_file_lines_buffer(conn, file_path, job_id)

        #Business validations
        result = run_business_validation_phase(conn, job_id)
        
        if result["fatal"]:
            job_repository.mark_job_as_rejected(conn, job_id, JobStatus.REJECTED.value, result["message"]) 
        
        elif result["errors"] > 0:
            job_repository.finalize_job_with_errors(conn, job_id, JobStatus.PROCESSED_WITH_ERRORS.value, result["errors"], result["message"])
        
        else:
            job_repository.finalize_job(conn, job_id, JobStatus.PROCESSED.value)

        conn.commit()
        return job_id 
        
    except Exception as e:
        conn.rollback()

        #best-effort mark as rejected
        if job_id is not None:
            try:
                job_repository.mark_job_as_rejected(conn, job_id, JobStatus.REJECTED.value, str(e))
                conn.commit()
            except Exception:
                pass
        raise
    
    finally:
        conn.close()


def run_business_validation_phase(conn, job_id) -> dict:
    """
    Returns:
    {
        fatal: bool,
        errors: int,
        message: str | None
    }
    """
    
    #TODO: Validate Header

    # Trailer = file-level (fatal)
    trailer_is_invalid = validate_trailer(job_id)
    if trailer_is_invalid:
        trailer_row_id, error_code, error_message = trailer_is_invalid
        insert_validation_error(conn, job_id, 'FILE_STRUCTURE', error_message, trailer_row_id, error_code)
        job_repository.mark_job_as_rejected(conn, job_id, JobStatus.REJECTED.value, error_message) 
        return {
            "fatal": True,
            "errors": 1,
            "message": error_message
        }
    
    # Detail = record-level (non-fatal)
    errors = validate_detail(job_id)
    if errors > 0:
        return {
            "fatal": False,
            "errors": errors,
            "message": "Detail lines with inconsistences"
        }
    
    return {
        "fatal": False,
        "errors": 0,
        "message": None
    }


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