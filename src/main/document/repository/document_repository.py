from src.config.mongodb import get_mongo_client
from src.main.document.dto.document import saveDocument, documentDetailDto
from datetime import datetime
from bson import ObjectId
from typing import List

##db에 문서 저장하기
def save_document(document : saveDocument) -> str:
    client = get_mongo_client()
    db = client['xrpedia-data']
    document_collection = db['document_collection'] #db 이름 지정

    document_id = document_collection.insert_one(document.model_dump()).inserted_id
    return str(document_id)

# db에서 문서 조회하기
def get_document(document_id: str) -> documentDetailDto:
    client = get_mongo_client()
    db = client['xrpedia-data']
    document_collection = db['document_collection']

    get_doc = document_collection.find_one({"_id": ObjectId(document_id)})

    # uploader = 

    doc = documentDetailDto(
        document_id=str(get_doc["_id"]),
        file_id=get_doc["file_id"],
        document_name=get_doc["document_name"],
        document_image_url= get_doc["document_image_url"],
        introduction= get_doc["introduction"],
        downloads= get_doc["downloads"],
        pageNumber= int(get_doc["pageNumber"], 0),
        upload_date= get_doc["upload_date"],
        uploader= get_doc["uploader_id"], #이거 추후에 변경해야 함함
        price= get_doc["price"],
        category= get_doc["category"],
        rating= get_doc["rating"])
    
    return doc

# 사용자 ID로 문서 목록 조회하기
def get_documents_by_user(user_id: str) -> List[documentDetailDto]:
    client = get_mongo_client()
    db = client['xrpedia-data']
    document_collection = db['document_collection']

    # 사용자 ID로 문서 필터링
    documents = document_collection.find({"uploader_id": user_id})
    
    result = []
    for doc in documents:
        document = documentDetailDto(
            document_id=str(doc["_id"]),
            file_id=doc["file_id"],
            document_name=doc["document_name"],
            document_image_url=doc["document_image_url"],
            introduction=doc["introduction"],
            downloads=doc["downloads"],
            pageNumber=doc["pageNumber"],
            upload_date=doc["upload_date"],
            uploader=doc["uploader_id"],
            price=doc["price"],
            category=doc["category"],
            rating=doc["rating"]
        )
        result.append(document)
    
    return result

# def get_user_name(user_id: str):
#     client = get_mongo_client()
#     db = client['xrpedia-data']
#     document_collection = db['wallet']

#     user = document_collection.find_one({"_id":ObjectId(user_id)})
    
#     return user[""]
