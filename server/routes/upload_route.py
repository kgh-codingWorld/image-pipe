import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from server.configs.log_config import logger
from server.models.image_DTO import UploadResponse
from server.utils.file_util import save_uploaded_file
from server.utils.meta_util import record_meta
from server.tasks.celery_worker import process_image_task, PROCESSING_METHODS

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_route(file:UploadFile = File(...), method:str=Form(...)):
    """
    업로드된 이미지를 서버에 저장 + Celery 작업 큐에 등록
    - 파일 저장 후 메타 정보 기록함
    - 비동기 처리 요청을 Celery에 전달
    - 작업 ID와 초기 상태 응답
    """
    # method 유효성 검사
    if not method or method not in PROCESSING_METHODS:
        raise HTTPException(status_code=400, detail=f"잘못된 처리 방식입니다: {method}")

    # 작업 ID 생성
    job_id = str(uuid.uuid4())
    logger.info(f"작업 ID 생성 완료: {job_id}")

    # 파일 저장
    save_uploaded_file(file, job_id)
    logger.info(f"파일 저장 완료: {job_id}")
    
    # 메타 정보 초기화
    record_meta(job_id=job_id, method=method, status="대기중")
    logger.info(f"메타 정보 기록 완료: {job_id}")
    
    # Celery 작업 큐로 전달 (delay: 즉시 실행 말고 큐에 등록만.)
    process_image_task.delay(job_id=job_id, method=method)
    logger.info(f"작업 큐에 등록 완료: {job_id}")

    return UploadResponse(
        job_id=job_id,
        status="대기중"
    )