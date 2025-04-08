from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR"))
RESULT_DIR = Path(os.getenv("RESULT_DIR"))
META_FILE = Path(os.getenv("META_FILE"))

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_URL = os.getenv("MINIO_URL")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
