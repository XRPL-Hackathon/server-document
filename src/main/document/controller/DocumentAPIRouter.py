import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.auth.dependencies import get_current_user
from src.main.document.service.document_service import save_document_service
from src.main.document.dto.document import documentRequestDto

router = APIRouter(
    prefix="/documents",
    tags=["문서 업로드"]
)

@router.post("")
async def uploadDocument(request: documentRequestDto, user_id: uuid.UUID = Depends(get_current_user)):
    try:
        document_id = await save_document_service(request, str(user_id))
        return document_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"문서 업로드 중 문제 발생: {str(e)}")
