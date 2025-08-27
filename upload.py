import boto3
import uuid
import os
from datetime import datetime, timezone

# ==============================
# Configuration
# ==============================
SOURCE_BUCKET = "myapp-source345234623546"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

s3_client = boto3.client("s3")


def get_content_type(filename):
    ext = filename.lower().split(".")[-1]
    if ext in ["jpg", "jpeg"]:
        return "image/jpeg"
    elif ext == "png":
        return "image/png"
    elif ext == "gif":
        return "image/gif"
    elif ext == "webp":
        return "image/webp"
    elif ext == "bmp":
        return "image/bmp"
    else:
        return "application/octet-stream"


def upload_image(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        raise ValueError("File too large. Max 10MB allowed.")

    content_type = get_content_type(file_path)
    filename = f"uploaded_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}{os.path.splitext(file_path)[1]}"

    with open(file_path, "rb") as f:
        s3_client.put_object(
            Bucket=SOURCE_BUCKET,
            Key=filename,
            Body=f,
            ContentType=content_type,
            Metadata={
                "uploaded-via": "local-uploader",
                "upload-timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    print(f"✅ Uploaded {file_path} → s3://{SOURCE_BUCKET}/{filename}")
    return filename


if __name__ == "__main__":
    file_path = input("Enter the path of the image you want to upload: ").strip()
    try:
        uploaded_key = upload_image(file_path)
        print(f"S3 Key: {uploaded_key}")
    except Exception as e:
        print(f"❌ Error: {e}")
