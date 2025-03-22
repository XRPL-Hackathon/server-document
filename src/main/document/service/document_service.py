#1. 사용자로부터 request를 받아온다.
#2. 이를 db에 저장한다.
#3. client에게 보낸다.

from src.main.document.repository.document_repository import  get_all_documents, save_document, get_document
from src.main.user.repository.UserRepository import get_user
from src.main.nft.service.nft_service import process_nft_issuance_with_response
from src.main.document.dto.document import saveDocument, documentRequestDto
from src.main.user.service import UserService
from datetime import datetime
import asyncio


# 사용자로부터 request 받아서 ~~
async def save_document_service(request: documentRequestDto, user_id: str) :
    upload_date = datetime.now()

    user = UserService.get_user_info(user_id)
    user_name = user["nickname"]

    saved = saveDocument(
        file_id = request.file_id,
        document_name = request.document_name,
        document_image_url="https://image일것 같아?",
        introduction=request.introduction,
        downloads=32,
        pageNumber=3,
        upload_date=upload_date,
        uploader=user_name,
        price=request.price,
        category=request.category,
        rating=4.0
    )

    #db에 저장하기
    document_id = save_document(saved)

    #point & grade 구하기
    user = get_user(user_id)
    point = user.get("point")
    grade = user.get("nft_grade")
    user_id = user.get("user_id")

    #point 올리기기
    point += 500

    #nft 발급하기
    await process_nft_issuance_with_response(user_id, grade, point)
    
    return document_id 

# 조회하기
async def get_document_detail(document_id: str):
    return get_document(document_id)

# 사용자의 모든 문서 목록 조회
async def get_documents():
    return get_all_documents()