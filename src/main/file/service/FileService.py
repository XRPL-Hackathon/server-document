import json
from src.main.file.repository.FileRepository import FileRepository
from fastapi import UploadFile, requests
import os
import uuid
from datetime import datetime, UTC
from dotenv import load_dotenv

load_dotenv()

class FileService:
    def __init__(self):
        self.file_repository = FileRepository()

    async def upload_file(self, file: UploadFile, user_id: str):
        """
        파일을 S3에 업로드하고 MongoDB에 파일 정보를 저장한 후 file_id를 반환합니다.
        """
        # 랜덤 파일명 생성 (충돌 방지)
        file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
        s3_key = f"{uuid.uuid4()}{file_extension}"
        
        # 파일 콘텐츠 읽기
        file_content = await file.read()
        
        # S3에 업로드
        s3_bucket = os.getenv("AWS_S3_BUCKET_NAME")
        result = self.file_repository.upload_to_s3(s3_bucket, s3_key, file_content, file.content_type)
        
        if not result:
            return None
        
        # MongoDB에 파일 정보 저장
        file_info = {
            "filename": file.filename,
            "s3_key": s3_key,
            "s3_bucket": s3_bucket,
            "content_type": file.content_type,
            "size": len(file_content),
            "upload_date": datetime.now(UTC),
            "owner_id": user_id,
            "download_count": 0
        }
        
        file_id = self.file_repository.save_file_info(file_info)

        # 파일 중복 체크 API 호출
        try:
            duplicate_check_url = "https://5erhg0u08g.execute-api.ap-northeast-2.amazonaws.com/ai-proxy/file-duplicate-checks"
            payload = {
                "user_id": user_id,
                "file_id": str(file_id)
            }
            headers = {"Content-Type": "application/json"}
            requests.post(duplicate_check_url, data=json.dumps(payload), headers=headers)
        except Exception as e:
            print(f"파일 중복 체크 API 호출 중 오류 발생: {str(e)}")
            
        return file_id
    
    def update_file_info(self, file_id: str, metadata: dict, user_id: str):
        """
        파일의 메타데이터를 업데이트합니다.
        """
        # 파일 소유자 확인
        file_info = self.file_repository.get_file_info_with_user(file_id)
        
        if not file_info:
            return None
        
        if file_info.get("owner_id") != user_id:
            return False
        
        # 메타데이터 업데이트
        metadata["updated_at"] = datetime.now(UTC)
        result = self.file_repository.update_file_info(file_id, metadata)
        return result

    def download_file(self, file_id: str):
        file_info = self.file_repository.get_file_info(file_id)

        if not file_info:
            return {
                "status": 404,
                "message": "파일을 찾을 수 없습니다.",
                "detail": "해당 file_key에 대한 S3 정보가 존재하지 않습니다."
            }
        
        s3_key = file_info["s3_key"]
        s3_bucket = file_info["s3_bucket"]
        presigned_url = self.file_repository.get_presigned_url(s3_bucket, s3_key)

        if not presigned_url:
            return {
                "status": 404,
                "message": "S3에서 파일을 찾을 수 없습니다.",
                "detail": "요청한 파일이 S3에 존재하지 않습니다."
            }
        
        self.file_repository.increment_download_count(file_id)

        return {
            "status": 200,
            "file_url": presigned_url
        }