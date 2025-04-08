import requests
from PIL import Image
from io import BytesIO

def download_image(url:str) -> Image.Image:
    """
    주어진 URL에서 이미지를 다운로드 → PIL 이미지 객첼고 반환
    """
    try:
        response = requests.get(url)
        return Image.open(BytesIO(response.content)) # BytesIO로 변환
    except Exception as e:
        raise ValueError(f"이미지 다운로드 실패: {e}")
