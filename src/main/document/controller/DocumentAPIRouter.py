import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.auth.dependencies import get_current_user
from src.main.document.service.document_service import save_document_service, get_document_detail, get_documents
from src.main.document.dto.document import documentRequestDto,documentDetailDto
from typing import List
router = APIRouter(
    prefix="/documents",
    tags=["문서 업로드"]
)

@router.get("", response_model=List[documentDetailDto])
async def getDocuments():
    try:
        return await get_documents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"문서 목록 조회 중 문제 발생: {str(e)}")

@router.post("")
async def uploadDocument(request: documentRequestDto, user_id: uuid.UUID = Depends(get_current_user)):
    try:
        document_id = await save_document_service(request, str(user_id))
        return document_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"문서 업로드 중 문제 발생: {str(e)}")

@router.get("/{document_id}", response_model=documentDetailDto)
async def getDocument(document_id: str):
    try:
        if not document_id:
            raise Exception(404, detail="문서를 찾을 수 없습니다.")
        return await get_document_detail(document_id)
    except Exception as e:
        raise HTTPException(500, detail=f"조회 실패: {str(e)}")