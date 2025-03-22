import os
import boto3
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV")
AWS_PROFILE = os.getenv("AWS_PROFILE")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_S3_REGION = os.getenv("AWS_S3_REGION")

if ENV == "local-profile":
    session = boto3.Session(profile_name=AWS_PROFILE)
    s3_client = session.client("s3")
elif ENV == "prod":
    s3_client = boto3.client(
        "s3",
        region_name=AWS_S3_REGION
    )
else:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_S3_REGION
    )