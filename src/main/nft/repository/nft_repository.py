from src.config.mongodb import get_mongo_client
from src.main.nft.dto.nft_dto import NftResponseDto
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
def save_nfts_bulk(response: NftResponseDto):
    client = get_mongo_client()
    db = client['xrpedia-data']
    nft_collection = db['nft']

    docs = [
        {
            "nft_id": r.nft_id,
            "user_wallet": r.user_wallet,
            "nft_grade": r.nft_grade,
            "transaction_hash": r.transaction_hash
            #nft_metadata_uri: r.metadata_uri
            #"issued_at": r.issued_at,
            #"expires_at": r.expires_at,
        }
        for r in NftResponseDto
    ]
    
    if docs: 
        nft_collection.insert_many(docs)