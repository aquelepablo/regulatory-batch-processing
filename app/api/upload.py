"""
Receives upload, stores temp file, calls orchestrator, returns job_id
"""
from fastapi import APIRouter, File, UploadFile
from app.processing.orchestrator import process_file
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
    if not (os.path.exists(path)):
        try:
            os.mkdir(path)
        except:
            raise RuntimeError("Folder tmp_uploads not created")

    full_path = os.path.join(path, file.filename)

    uploaded_file = await file.read()

    with open(full_path, "wb") as f:
        f.write(uploaded_file)
        
    return full_path
