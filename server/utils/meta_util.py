import json
from datetime import datetime
from server.configs.config import META_FILE

# 메타 정보 파일 경로
if not META_FILE.exists():
    META_FILE.write_text("[]") # 빈 리스트로 초기화시킴

def record_meta(job_id:str,method:str,status:str):
    """
    작업 메타 저오를 meeta.json에 기록
    기존 내용을 읽고 새 job 항목 append..
    - 작업 ID, 처리 방식, 상태, 생성 시간 등 포함
    """
    with META_FILE.open("r+", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

        entry = {
            "job_id": job_id,
            "status": status,
            "method": method,
            "created_at": datetime.now().isoformat(),
            "result_url": None,
            "error_message": None
        }

        data.append(entry)

        f.seek(0)
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.truncate()

def update_meta_status(job_id:str,status:str,result_url:str=None):
    """
    지정된 작업 ID의 상태 갱신 _ 결과 이미지 url 저장(옵션임, 상태에 따라 none으로 저장될 수도 있음)
    """
    with META_FILE.open("r+", encoding="utf-8") as f:
        data = json.load(f)
        for job in data:
            if job["job_id"] == job_id:
                job["status"] = status
                if result_url:
                    job["result_url"] = result_url
                break
        f.seek(0)
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.truncate()

def get_meta_by_job_id(job_id:str):
    """
    작업 ID에 해당하는 메타 정보 조회
    - 존재하지 않으면 None 반환
    """
    with META_FILE.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return None

        for job in data:
            if job.get("job_id") == job_id:
                return job
        return None

def record_error(job_id: str, error_message: str):
    """
    작업 실패 시 상태를 실패로 업데이트 + 에러 메시지 기록
    """
    with META_FILE.open("r+", encoding="utf-8") as f:
        data = json.load(f)
        for job in data:
            if job["job_id"] == job_id:
                job["status"] = "실패"
                job["error_message"] = error_message
                break
        f.seek(0)
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.truncate()
