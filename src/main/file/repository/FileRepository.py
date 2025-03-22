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

    def get_file_info(self, file_id: str):
        return self.files_collection.find_one(
            {"_id": ObjectId(file_id)},
            {"s3_key": 1, "s3_bucket": 1}
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