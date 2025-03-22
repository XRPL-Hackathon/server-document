from bson import ObjectId
import boto3
from botocore.exceptions import ClientError
from src.config.S3Config import s3_client
from src.config.mongodb import get_mongo_client

class FileRepository:
    def __init__(self):
        client = get_mongo_client()
        self.db = client["xrpedia-data"]
        self.files_collection = self.db["files"]

    def upload_to_s3(self, s3_bucket: str, s3_key: str, file_content: bytes, content_type: str):
        """S3에 파일을 업로드합니다."""
        try:
            s3_client.put_object(
                Bucket=s3_bucket,
                Key=s3_key,
                Body=file_content,
                ContentType=content_type
            )
            return True
        except ClientError:
            return False

    def save_file_info(self, file_info: dict):
        """파일 정보를 MongoDB에 저장하고 file_id를 반환합니다."""
        result = self.files_collection.insert_one(file_info)
        return str(result.inserted_id)

    def update_file_info(self, file_id: str, metadata: dict):
        """파일 메타데이터를 업데이트합니다."""
        result = self.files_collection.update_one(
            {"_id": ObjectId(file_id)},
            {"$set": metadata}
        )
        return result.modified_count > 0

    def get_file_info(self, file_id: str):
        """파일 정보를 조회합니다."""
        return self.files_collection.find_one(
            {"_id": ObjectId(file_id)},
            {"s3_key": 1, "s3_bucket": 1}
        )

    def get_file_info_with_user(self, file_id: str):
        """파일 정보와 사용자 ID를 함께 조회합니다."""
        return self.files_collection.find_one(
            {"_id": ObjectId(file_id)},
            {"s3_key": 1, "s3_bucket": 1, "owner_id": 1}
        )

    def get_presigned_url(self, s3_bucket: str, s3_key: str):
        try:
            s3_client.head_object(Bucket=s3_bucket, Key=s3_key)
            return s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": s3_bucket, "Key": s3_key},
                ExpiresIn=3600,
            )
        except ClientError as e:
            # 파일 존재 X : 404 반환
            if e.response["Error"]["Code"] == "404":
                return None
            else:
                raise e

    # MongoDB에서 해당 파일의 다운로드 횟수 +1        
    def increment_download_count(self, file_id: str):
        self.files_collection.update_one(
            {"_id": ObjectId(file_id)},
            {"$inc": {"download_count": 1}}
        )