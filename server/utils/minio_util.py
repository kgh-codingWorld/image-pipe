from minio import Minio
from pathlib import Path
from server.configs.config import(
    MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_URL, MINIO_BUCKET
)

# MinIO 클라이언트 설정
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # 로컬에서는 https 안 쓰니까 False!!
)

def upload_to_minio(file_path: Path, object_name: str) -> str:
    """
    MinIO에 이미지 업로드 후 접근 가능한 URL 반환
    """
    if not minio_client.bucket_exists(MINIO_BUCKET):
        raise ValueError(f"버킷 '{MINIO_BUCKET}'이 존재하지 않음")

    minio_client.fput_object(
        MINIO_BUCKET,
        object_name,
        str(file_path),
        content_type="image/png"
    )

    return f"{MINIO_URL}/{MINIO_BUCKET}/{object_name}"
