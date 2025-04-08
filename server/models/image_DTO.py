from pydantic import BaseModel
from typing import Optional

class UploadResponse(BaseModel):
    job_id: str
    status: str

class StatusResponse(BaseModel):
    job_id: str
    status: str
    method: str
    created_at: str
    result_url: Optional[str]
    error_message: Optional[str]
