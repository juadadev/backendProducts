import os

import boto3


def read_secret(secret_name):
    path = f"/run/secrets/{secret_name}"
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    return os.getenv(secret_name)


AWS_REGION = read_secret("AWS_REGION")
AWS_ACCESS_KEY_ID = read_secret("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = read_secret("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = read_secret("S3_BUCKET_NAME")

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
