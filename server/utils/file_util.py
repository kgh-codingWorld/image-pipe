import uuid, shutil
from fastapi import UploadFile
from pathlib import Path
from PIL import Image
from server.configs.config import UPLOAD_DIR

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# def save_temp_file(image:str)->tuple[str,str]:
#     job_id = str(uuid.uuid4())
#     path = UPLOAD_DIR / f"{job_id}.png"

#     if isinstance(image, Image.Image):
#         image.save(path)
#     else:
#         Image.fromarray(image).save(path)

#     return job_id, str(path)

def save_uploaded_file(file:UploadFile, job_id:str)->str:
    """
    FastAPI에서 받은 UploadFile을 지정된 위치에 저장
    - 저장 경로: static/uploads/{job_id}.original.png
    """
    file_path = UPLOAD_DIR / f"{job_id}.original.png"
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return str(file_path)