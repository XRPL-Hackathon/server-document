from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from src.auth.dependencies import get_current_user
from src.main.file.service.FileService import FileService
import uuid
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/files",
    tags=["files"],
)

class FileMetadata(BaseModel):
    filename: str
    description: Optional[str] = None
    tags: Optional[list[str]] = None

# 파일 업로드
@router.post("")
async def upload_file(
    file: UploadFile = File(...),
    user_id: uuid.UUID = Depends(get_current_user),
    file_service: FileService = Depends()
):
    file_id = await file_service.upload_file(file, str(user_id))
    return {"file_id": file_id}

# 파일 정보 업데이트
@router.post("/{file_id}/info")
async def update_file_info(
    file_id: str,
    file_metadata: FileMetadata,
    user_id: uuid.UUID = Depends(get_current_user),
    file_service: FileService = Depends()
):
    result = file_service.update_file_info(file_id, file_metadata.dict(), str(user_id))
    if not result:
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
    return {"status": "success", "file_id": file_id}

# S3에서 파일 다운로드
@router.get("/{file_id}")
async def download_file(
    file_id: str, 
    user_id: uuid.UUID = Depends(get_current_user),
    file_service: FileService = Depends()
):
    return file_service.download_file(file_id)