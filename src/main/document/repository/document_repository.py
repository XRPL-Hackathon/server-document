from src.config.mongodb import get_mongo_client
from src.main.document.dto.document import saveDocument
from datetime import datetime

##db에 문서 저장하기
def save_document(document : saveDocument) -> str:
    client = get_mongo_client()
    db = client['xrpedia-data']
    document_collection = db['document_collection'] #db 이름 지정

    result = document_collection.insert_one(document.model_dump())

    return str(result.inserted_id)