"""
Receives upload, stores temp file, calls orchestrator, returns job_id
"""
from fastapi import APIRouter, File, UploadFile
from app.processing.orchestrator import process_file, get_job_status
import os


router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> dict:
    file_path = await save_temp_file(file)
    job_id = process_file(file_path)
    return {"job_id": job_id}

async def save_temp_file(file: UploadFile) -> str:
    #READ THE FILE
    #STORE IT IN tmp_uploads

    path = "./tmp_uploads/"
    os.makedirs(path, exist_ok=True)
    full_path = os.path.join(path, file.filename)

    with open(full_path, "wb") as out:
        while True:
            chunk = await file.read(1024 * 1024) #1 MB
            if not chunk:
                break
            out.write(chunk)
    return full_path

@router.get("/status/{job_id}")
def get_status(job_id: int):
    return get_job_status(job_id)
