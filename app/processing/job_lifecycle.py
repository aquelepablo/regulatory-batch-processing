def create_job(conn, file_name: str) -> int:
    pass
def start_job(conn, job_id: int) -> None:
    pass
def reject_job(conn, job_id: int, error_message: str, error_code: str | None = None) -> None:
    pass
def finalize_job(conn, job_id: int) -> None:
    pass
