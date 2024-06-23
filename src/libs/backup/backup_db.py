import os
from os.path import isfile, join

import boto3
from src.commons.configs.config import get_app_settings

settings = get_app_settings()


def upload_backup_file_to_S3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        region_name=settings.s3_region,
    )

    only_files = [f for f in os.listdir("./backups") if isfile(join("./backups", f))]

    try:
        for filename in only_files:
            if "sql.gz" in filename:
                s3.upload_file(
                    f"./backups/{filename}",
                    settings.s3_bucket_name,
                    f"backups/{filename}",
                )
                os.remove(f"./backups/{filename}")

    except Exception as e:
        print(f"Error when upload file to S3. error = {e}")


upload_backup_file_to_S3()
