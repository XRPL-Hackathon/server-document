from fastapi import APIRouter, Depends
from src.auth.dependencies import get_current_user
from src.main.file.service.FileService import FileService
import uuid

router = APIRouter(
    prefix="/file",
    tags=["file"],
)

# S3에서 파일 다운로드
@router.get("/{file_id}")
async def download_file(
    file_id: str, 
    user_id: uuid.UUID = Depends(get_current_user),
    file_service: FileService = Depends()
):
    return file_service.download_file(file_id)