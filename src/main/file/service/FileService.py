from src.main.file.repository.FileRepository import FileRepository

class FileService:
    def __init__(self):
        self.file_repository = FileRepository()

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