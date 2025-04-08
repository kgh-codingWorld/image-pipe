from celery import Celery
from pathlib import Path
from frontend.configs.config import BASE_URL
from server.configs.log_config import logger
from server.configs.config import CELERY_BROKER_URL, RESULT_DIR
from server.utils.meta_util import update_meta_status, record_error
from server.utils.processing_util import (
    apply_processing_sync,
    apply_processing_threaded,
    apply_processing_multiprocess,
)
from server.utils.minio_util import upload_to_minio

# 처리 방식 문자열을 실제 함수에 매핑
PROCESSING_METHODS = {
    "싱글 스레드": apply_processing_sync,
    "멀티 스레드": apply_processing_threaded,
    "멀티 프로세스": apply_processing_multiprocess
}

# Celery 인스턴스 생성
app = Celery("tasks", broker=CELERY_BROKER_URL)

# 결과 저장 디렉토리 생성(존재하지 않을 때)
RESULT_DIR.mkdir(parents=True, exist_ok=True)

@app.task
def process_image_task(job_id: str, method: str):
    """
    Celery 비동기 작업 함수
    - 지정된 처리 방식에 따라 이미지 처리를 실행
    - 처리 결과를 MinIO에 저장하고, 메타 정보를 갱신
    """
    try:
        logger.info(f"작업 시작: {job_id} | method={method}")

        # 경로 설정
        input_path = Path(f"static/uploads/{job_id}.original.png")
        output_path = Path(f"static/results/{job_id}.png")

        logger.info(f"[CELERY] Input: {input_path} | Exists: {input_path.exists()}")

        # 상태를 처리중으로 업데이트
        update_meta_status(job_id, "처리중")

        # dict mapping 방식 - 처리 함수 선택 및 실행
        process_fn = PROCESSING_METHODS.get(method)
        if not process_fn:
            raise ValueError(f"지원되지 않는 처리 방식: {method}")

        process_fn(input_path, output_path)

        # 결과를 MinIO에 업로드하고 URL을 획득함
        object_name = f"{job_id}.png"
        result_url = upload_to_minio(output_path, object_name)

        # 상태를 완료로 업데이트 + url
        update_meta_status(job_id, "완료", result_url)

        logger.info(f"작업 성공: {job_id} → {result_url}")

    except Exception as e:
        logger.exception(f"작업 실패 {job_id}")
        record_error(job_id, str(e))
