from pydantic import BaseModel
from datetime import datetime

class saveDocument(BaseModel):
    file_id: str
    document_name: str
    document_image_url: str # 더미
    introduction: str 
    downloads: int # 더미
    pageNumber: int # 더미
    upload_date: datetime
    uploader_id: str 
    price: float 
    category: str

class documentRequestDto(BaseModel):
    file_id: str
    document_name: str
    introduction: str
    price: float
    category: str