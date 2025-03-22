from src.config.mongodb import get_mongo_client
from src.main.nft.dto.nft_dto import NftSaveDto
from datetime import datetime


#db에 nft_grade 집어넣기랑 point 갱신하기
def save_userDB_nft(user_id:str, nft_grade: str, point: int):
    client = get_mongo_client()
    db = client['xrpedia-data']
    nft_collection = db['wallets']

    if not user_id:
        raise Exception(404, detail="회원 정보를 찾을 수 없습니다.")
    
    nft_collection.update_one(
        {"user_id": user_id}, #필터
        {"$set": {"point": point, "nft_grade": nft_grade}}
    )



# repository/nft_repository.py
def save_nfts_bulk(response: NftSaveDto):
    client = get_mongo_client()
    db = client['xrpedia-data']
    nft_collection = db['nft']

    nft_collection.insert_one(response)