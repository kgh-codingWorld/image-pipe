import requests
from frontend.configs.config import BASE_URL
from server.configs.log_config import logger

def post_upload(image_file:str, method:str):
    """
    업로드 함수 엔드포인트 매핑
    """
    logger.info(f"image_file: {image_file}")
    logger.info(f"method: {image_file}")
    logger.info(f"is file path: {isinstance(image_file, str)}")

    with open(image_file, "rb") as f:
        files = {"file": ("uploaded.png", f, "image/png")}
        data = {"method": method}
        response = requests.post(f"{BASE_URL}/upload", files=files, data=data)
        
    logger.info(f"Response: {response.status_code}, {response.text}")
    return response.json()["job_id"]