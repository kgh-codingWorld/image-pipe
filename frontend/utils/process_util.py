import os
from frontend.utils.upload_util import post_upload
from frontend.services.polling_service import poll_until_done

def process_image(image_file:str, method:str):
    """
    Gradio UI에서 실행할 조립 함수
    - 이미지 파일을 FastAPI로 업로드
    - job_id로 상태 polling
    - 결과 반환
    """
    # method 비어있음
    if not method:
        return "처리 방식을 선택해주세요.", None

    # 파일 경로 유효성 검사
    if not os.path.exists(image_file):
        return "이미지가 업로드되지 않았습니다.", None

    # 이미지 업로드 후 Polling 작업 시작
    job_id = post_upload(image_file, method)
    return poll_until_done(job_id)
