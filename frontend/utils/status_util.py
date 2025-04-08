import requests
from frontend.configs.config import BASE_URL

def get_status(job_id: str) -> dict:
    """ 
    상태 확인 함수 엔드포인트 매핑
    """
    response = requests.get(f"{BASE_URL}/status/{job_id}")
    return response.json()

