from src.config.mongodb import get_mongo_client

from typing import Optional
from src.config.mongodb import get_mongo_client

class UserRepository:
    def __init__(self):
        client = get_mongo_client()
        self.db = client["xrpedia-data"]
        self.wallets_collection = self.db["wallets"]

    def find_wallets_by_user_id(self, user_id: str) -> list:
        wallets = list(self.wallets_collection.find({"user_id": user_id}, {"_id": 0}))
        return wallets if wallets else []
#db에서 user 가져오기
    def get_user(self, user_id: str) -> str:
        client = get_mongo_client()
        db = client['xrpedia-data']
        nft_collection = db['wallets']

        if not user_id:
            raise Exception(404, detail="회원 정보를 찾을 수 없습니다.")
    
    
        user = nft_collection.find_one({"user_id": user_id})

        if not user:
            raise Exception(404, detail="해당 유저를 찾을 수 없습니다.")
    
        # ObjectId는 JSON 직렬화가 안 되므로 필요 시 string으로 바꿔줍니다
        user["_id"] = str(user["_id"])

        return user