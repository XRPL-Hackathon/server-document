#1. 사용자로부터 request를 받아온다.
#2. 이를 db에 저장한다.
#3. client에게 보낸다.

from src.main.document.repository.document_repository import save_document, get_document
from src.main.document.dto.document import saveDocument, documentRequestDto
from datetime import datetime
import asyncio


# 사용자로부터 request 받아서 ~~
async def save_document_service(request: documentRequestDto, user_id: str) :
    upload_date = datetime.now()

    saved = saveDocument(
        file_id = request.file_id,
        document_name = request.document_name,
        document_image_url="https://image일것 같아?",
        introduction=request.introduction,
        downloads=32,
        pageNumber=3,
        upload_date=upload_date,
        uploader_id=user_id,
        price=request.price,
        category=request.category,
        rating=4.0
    )

    #db에 저장하기
    document_id = save_document(saved)

    return document_id 

# 조회하기
async def get_document_detail(document_id: str):
    return get_document(document_id)