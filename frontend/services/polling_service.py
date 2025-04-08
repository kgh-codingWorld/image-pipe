import time
from frontend.utils.status_util import get_status
from frontend.utils.download_util import download_image
from server.configs.log_config import logger

def poll_until_done(job_id:str, max_wait:int=30):
    """
    Gradio에서 상태를 폴링하며 결과 기다림
    - 최대 시간 동안 반복적으로 상태 확인
    - 완료 후 이미지 다운로드 그리고 반환
    - 실패 상태 또는 타임아웃 발생 시 에러 메시지 반환
    """
    for _ in range(max_wait):
        logger.info("polling 시작")
        time.sleep(1)

        # /status/{job_id} 호출
        status_info = get_status(job_id)
        if not status_info:
            raise ValueError(f"작업 상태 확인 실패: {job_id}")
        logger.info(f"status_info: {status_info}")

        status = status_info.get("status")
        logger.info(f"status: {status}")

        if status == "완료":
            img = download_image(status_info["result_url"])
            return f"처리 완료: 작업 ID {job_id}", img

        elif status == "실패":
            return f"처리 실패: {status_info.get('error_message')}", None

    return f"시간 초과: 작업 ID {job_id}", None
