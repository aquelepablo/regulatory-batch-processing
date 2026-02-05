"""
Docstring for app.persistence.job_repository
insert_job
update_job_status
update_job_counters
get_job_error_count
"""

def insert_job(conn, file_name) -> int:
    pass
def set_job_processing(conn, job_id) -> None:
    pass
def set_job_as_rejected(conn, job_id, error_message) -> None:
    pass
def update_job_counters(conn, job_id, total_records, total_errors) -> None:
    pass
def set_job_final_status(conn, job_id, final_status, finished_at) -> None:
    pass
def get_job_error_count(conn, job_id) -> int:
    pass