from pydantic import BaseModel
from typing import Dict
from datetime import datetime

#Nft 를 ResponseDto (checking 용)
class NftResponseDto(BaseModel):
    user_wallet_id: str
    point: int
    nft_id: str
    nft_grade: str
    transaction_hash: str
    nft_metadata_uri: str
    issued_at: datetime
    expired_at: datetime

#db 는 따로 wallet에 저장하기
class NftSaveDto(BaseModel):
    id: str
    user_wallet: str
    nft_id: str
    nft_grade: str
    transaction_hash: str
    #nft_metadata_uri: str
    issued_at: datetime
    expired_at: datetime