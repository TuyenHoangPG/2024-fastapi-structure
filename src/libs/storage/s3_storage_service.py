import os
from uuid import uuid4

import boto3
from werkzeug.utils import secure_filename

from src.commons.configs.config import get_app_settings
from src.commons.constants.message import ERROR_MESSAGE
from src.commons.middlewares.exception import AppExceptionCase

settings = get_app_settings()
s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.s3_access_key,
    aws_secret_access_key=settings.s3_secret_key,
    region_name=settings.s3_region,
)


class S3StorageService:
    def upload_file_to_s3(self, file, path, file_name=None, content_type=None):
        filename = file_name if file_name else secure_filename(file.filename)
        key = f"{path}/{uuid4()}-{filename}"

        try:
            s3.upload_fileobj(
                file,
                Bucket=settings.s3_bucket_name,
                Key=key,
                ExtraArgs={
                    "ContentType": content_type if content_type else file.content_type
                },
            )

        except Exception as e:
            raise AppExceptionCase(
                context={"reason": ERROR_MESSAGE.SERVER_ERROR, "code": e.code},
                status_code=500,
            )

        return {
            "key": key,
            "filename": filename,
            "file": file,
        }

    def generate_signed_url(self, key):
        expiration_seconds = 60 * 60  # 1 hour
        signed_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.s3_bucket_name, "Key": key},
            ExpiresIn=expiration_seconds,
        )

        return signed_url

    def get_object(self, key):
        response = s3.get_object(Bucket=settings.s3_bucket_name, Key=key)
        return response
