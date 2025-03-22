from src.main.nft.dto.nft_dto import NftResponseDto, NftSaveDto
from src.main.user.repository.UserRepository import get_user
from src.main.nft.repository.nft_repository import save_userDB_nft, save_nfts_bulk 
from datetime import datetime, timezone, timedelta
import asyncio

# XRPL 관련 모듈
#pip install xrpl-py + python -m poetry add xrpl.py
from xrpl.asyncio.transaction import submit_and_wait
from xrpl.models.transactions.nftoken_mint import NFTokenMint, NFTokenMintFlag
from xrpl.asyncio.wallet import generate_faucet_wallet
from xrpl.wallet import Wallet
from xrpl.clients import JsonRpcClient
import json


# XRPL 설정
print("Connecting to Testnet...")
JSON_RPC_URL = "https://s.devnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)

# 등급별 Taxon 값 설정 (NFT 분류 번호)
NFT_GRADE_TAXON = {
    "platinum": 4,
    "gold": 3,
    "silver": 2,
    "bronze": 1  # 기본값
}

# 테스트 지갑 생성 (테스트넷용)
# generate~ 함수는 내부적으로 비동기 함수임(asyncio.run()) -> ㅇ미 비동기에서 비동기로 겹침침
async def generate_wallet ():
    wallet = await generate_faucet_wallet(client=client)
    return wallet, wallet.address

# XRPL 기반 NFT 민팅(XRPL 에서 NFT를 실제로 발급(MINt) 하는 핵심 함수)
# 개별 사용자 1명에게 NFT를 발급하는 함수
async def mint_nft_on_xrpl(user, grade, issuser_wallet, issuserAddr):
    issued_at = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    expired_at = issued_at + timedelta(days=180)

    mint_tx = NFTokenMint(
        account=issuserAddr, # 발급자(대표자)
        nftoken_taxon=NFT_GRADE_TAXON[grade], # NFT 분류 Id (의미를 부여) grade에 따라 자동 적용용
        flags=NFTokenMintFlag.TF_TRANSFERABLE # NFT 가 전송 가능한 것인지 여부 설정정
        )

    try:
        # xrpl에서 해당 정보를 트랜잭션에 넘기기기
        # submit_and_wait(transaction, client(노드 클라이언트 자체), wallet(서명에 사용될 지갑 객체체))
        response = await submit_and_wait(transaction=mint_tx, client=client, wallet=issuser_wallet)
        # transaction 처리 결과
        result = response.result

        # 트랜잭션 해시 추출(트랜잭션 고유 ID) -> 블록 탐색기에서 이 해시로 NFT 상태 조회 가능
        tx_hash = result['hash']
        if not tx_hash or not isinstance(tx_hash, str):
            raise Exception("트랜잭션 해시를 정상적으로 받지 못했습니다.")
        
        # NFT ID 파싱을 위함
        nft_id = ""
        
        for node in result['meta']['AffectedNodes']:
            node_data = node.get("CreatedNode") or node.get("ModifiedNode")
            if node_data and node_data["LedgerEntryType"] == "NFTokenPage":
                tokens = node_data.get("NewFields", {}).get("NFTokens") or node_data.get("FinalFields", {}).get("NFTokens")
                if tokens:
                    for token in tokens:
                        nft = token.get("NFToken")
                        if nft and "NFTokenID" in nft:
                            nft_id = nft["NFTokenID"]
                            break
            if nft_id:
                break

        if not nft_id:
            raise Exception("NFT ID 추출 실패")

        return {
            "user_wallet": user.get("_id"),
            "point": user.get("point"),
            "nft_id": nft_id,
            "nft_grade": user.get("nft_grade"),
            "transaction_hash": tx_hash,
            "issued_at": issued_at,
            "expired_at": expired_at
        }
    
    except Exception as e:
        print(f"NFT 민팅 실패: {e}")
        return None

#grade 다음 단계 반환
async def next_grade(grade:str)-> str:
    if not grade: 
        raise Exception(422, detail="none 입니다.")
    
    if grade =="bronze":
        return "silver"
    elif grade == "silver":
        return "gold"
    elif grade == "gold":
        return "platinum"
    elif grade == "platinum":
        return "platinum"  # 이미 최고 등급이면 그대로 유지
    else:
        raise Exception("400: 유효하지 않은 등급입니다.")

# 전체 로직
async def process_nft_issuance_with_response(user_id: str, origin_grade:str, point: int):
    issuser_wallet, issuserAddr = await generate_wallet()

    #grade 다음 단계 구하기 로직 
    grade = await next_grade(origin_grade)

    #user_id
    user = get_user(user_id)

    # 하나 발급 -> grade의 다음 단계로 받아오게끔 하기
    result = await mint_nft_on_xrpl(user, grade, issuser_wallet, issuserAddr)

    # DB 저장용 객체 변환
    nft_records = NftSaveDto(
            nft_id=result["nft_id"],
            user_wallet=result["user_wallet"],
            nft_grade=result["nft_grade"],
            transaction_hash=result["transaction_hash"],
            issued_at=result["issued_at"],
            expired_at=result["expired_at"]
        )
    save_nfts_bulk(nft_records.model_dump())

    #user에도 반영되도록 구현현
    save_userDB_nft(user_id, grade, point)

    # DTO 변환
    print(NftResponseDto(
            user_wallet_id=result["user_wallet"],
            point=result["point"],
            nft_id=result["nft_id"],
            nft_grade=result["nft_grade"],
            transaction_hash=result["transaction_hash"],
            issued_at=result["issued_at"],
            expired_at=result["expired_at"]
        ))