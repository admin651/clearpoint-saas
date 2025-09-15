import os, uuid
from typing import Tuple
from .config import settings

LOCAL_DIR = "./storage"

def ensure_local_dir():
    os.makedirs(LOCAL_DIR, exist_ok=True)

def save_local(content: bytes, filename: str) -> str:
    ensure_local_dir()
    key = f"{uuid.uuid4()}_{filename}"
    path = os.path.join(LOCAL_DIR, key)
    with open(path, "wb") as f:
        f.write(content)
    return key

def load_local(key: str) -> bytes:
    path = os.path.join(LOCAL_DIR, key)
    with open(path, "rb") as f:
        return f.read()

# S3 hooks (optional)
def save_bytes(content: bytes, filename: str) -> str:
    if settings.s3_bucket and settings.aws_access_key_id and settings.aws_secret_access_key:
        # TODO: implement boto3 upload; return s3 key
        # Stub fallback:
        return save_local(content, filename)
    else:
        return save_local(content, filename)

def load_bytes(key: str) -> bytes:
    if settings.s3_bucket and settings.aws_access_key_id and settings.aws_secret_access_key:
        # TODO: implement boto3 download
        return load_local(key)
    return load_local(key)
