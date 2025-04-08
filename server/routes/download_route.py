from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from server.configs.log_config import logger
from server.utils.meta_util import get_meta_by_job_id
from pathlib import Path

router = APIRouter()

@router.get("/download/{job_id}", response_class=FileResponse)
async def download_result(job_id:str):
    """
    작업 ID를 기반으로 처리된 결과 이미지를 반환
    - 수틀릴 시 404 에러 반환
    - 최종 이미지 파일을 FileResponse로 전달
    """
    logger.info(f"다운로드 요청: {job_id}")
    meta = get_meta_by_job_id(job_id)
    if not meta:
        raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다.")

    result_url = meta.get("result_url")
    if not result_url:
        raise HTTPException(status_code=404, detail="아직 결과가 없습니다.")

    file_path = Path(result_url)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")

    return FileResponse(path=file_path, filename=file_path.name, media_type="image/png")
