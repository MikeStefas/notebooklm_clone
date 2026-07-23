import os
import io
import boto3
from botocore.exceptions import ClientError
from fastapi.responses import StreamingResponse

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "password123")

s3_client = boto3.client(
    "s3",
    endpoint_url=f"http://{MINIO_ENDPOINT}",
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    region_name="us-east-1"
)

def create_bucket(bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except ClientError:
        s3_client.create_bucket(Bucket=bucket_name)

def upload_to_minio(project_id, file_id, file, bucket_name):
    filename = file.filename or "unnamed"
    key = f"{project_id}/{file_id}/{filename}"
    try:
        s3_client.upload_fileobj(Bucket=bucket_name, Key=key, Fileobj=file.file)
        return True
    except ClientError as e:
        print(e)
        return False


def create_presigned_get_url(bucket_name: str, object_name: str) -> str | None:
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_name,
                'ResponseContentType': 'application/pdf'
            },
            ExpiresIn=60,
        )
        return response
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None

def create_presigned_post(bucket_name: str, object_name: str, content_type: str = None, expiration: int = 60) -> dict | None:
    try:
        fields = {}
        conditions = []
        if content_type:
            fields["Content-Type"] = content_type
            conditions.append({"Content-Type": content_type})

        response = s3_client.generate_presigned_post(
            bucket_name,
            object_name,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=expiration
        )
        return response
    except ClientError as e:
        print(f"Error generating presigned POST: {e}")
        return None


def delete_from_minio(project_id, file_id, bucket_name):
    prefix = f"{project_id}/{file_id}/"
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        contents = response.get('Contents', [])
        for obj in contents:
            s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
        return True
    except ClientError as e:
        print(e)
        return False