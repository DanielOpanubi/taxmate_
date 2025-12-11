from minio import Minio
import os
from io import BytesIO

MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY", "minioadmin123")
BUCKET = "invoices"

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# ensure bucket exists
if not client.bucket_exists(BUCKET):
    client.make_bucket(BUCKET)

def upload_file_to_minio(filename: str, data: bytes) -> str:
    obj_name = filename
    client.put_object(BUCKET, obj_name, BytesIO(data), length=len(data))
    # return presigned URL (valid short time) or object path
    return f"{MINIO_ENDPOINT}/{BUCKET}/{obj_name}"
