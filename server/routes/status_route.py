from fastapi import APIRouter, HTTPException
from server.configs.log_config import logger
from server.models.image_DTO import StatusResponse
from server.utils.meta_util import get_meta_by_job_id

router = APIRouter()

@router.get("/status/{job_id}", response_model=StatusResponse)
async def get_status(job_id: str):
    """
    주어진 작업 ID에 대한 처리 상태를 반환
    - 작업이 존재하지 않을 시 404 에러 반환
    - 메타 파일에서 상태, 처리 방식 생성 시간 등 조회
    """
    logger.info(f"상태 조회: {job_id}")
    meta = get_meta_by_job_id(job_id)
    if not meta:
        raise HTTPException(status_code=404, detail=f"작업을 찾을 수 없습니다: {job_id}")

    return StatusResponse(
        job_id=job_id,
        status=meta.get("status"),
        method=meta.get("method"),
        created_at=meta.get("created_at"),
        result_url=meta.get("result_url"),
        error_message=meta.get("error_message")
    )
