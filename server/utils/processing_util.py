import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import threading

# 
# 처리 단위가 분리되어 있음(병렬 처리 가능해짐)
# 처리 방식이 추상화됨
# 실행 방식이 동적으로 선태 가능

def _process_image_pipeline(input_path: Path, output_path: Path):
    """
    공통 이미지 처리 파이프라인 함수
    - 흑백 변환, 썸네일 생성, 워터마크 삽입 후 저장
    """
    # 열기
    try:
        img = Image.open(input_path)
    except Exception as e:
        raise RuntimeError(f"이미지 열기 실패: {e}")
    
    # 흑백 변환
    img = img.convert("L")

    # 썸네일
    img.thumbnail((256, 256))  # 정사각 썸네일

    # 워터마크
    draw = ImageDraw.Draw(img)
    watermark = "ImagePipe"
    position = (10, img.height - 20)
    draw.text(position, watermark, fill=200)

    # 저장
    try:
        img.save(output_path)
    except Exception as e:
        raise RuntimeError(f"이미지 저장 실패: {e}")

def apply_processing_sync(input_path: Path, output_path: Path):
    """
    싱글 스레드 방식
    """
    _process_image_pipeline(input_path, output_path)

def apply_processing_threaded(input_path: Path, output_path: Path):
    """
    멀티 스레드 방식
    """
    def worker():
        _process_image_pipeline(input_path, output_path)

    t = threading.Thread(target=worker)
    t.start()
    # 동기화
    t.join()

import os

def apply_processing_multiprocess(input_path: Path, output_path: Path):
    """
    멀티 프로세스 방식 - Unix 계열에서만 동작하고 Window는 NotImplementedError 뜸 → subprocess로 가능
    """
    # if os.name == "nt":
    #     raise NotImplementedError("Windows 환경에서 멀티프로세스는 지원하지 않음.")

    subprocess.run(
        [sys.executable, "server/services/multiprocess_worker.py", str(input_path), str(output_path)],
        check=True
    )

