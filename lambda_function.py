import boto3
import urllib.request
import uuid
from datetime import datetime, timezone

SOURCE_BUCKET = "<YOUR_S3_SOURCE_NAME>"
DEST_BUCKET = "<YOUR_S3_SOURCE_NAME>"
FLASK_SERVER_URL = "http://<EC2_PUBLIC_IP>:5000/process"

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        key = record['s3']['object']['key']
        process_image(key)

def process_image(key):
    # تنزيل الصورة من Source S3
    obj = s3_client.get_object(Bucket=SOURCE_BUCKET, Key=key)
    file_data = obj['Body'].read()

    # إرسال الصورة لـ Flask Server
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{key}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(FLASK_SERVER_URL, data=body)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    
    with urllib.request.urlopen(req) as response:
        processed_data = response.read()

    # رفع الصورة المعالجة إلى Destination S3
    new_filename = f"{uuid.uuid4()}.jpg"
    s3_client.put_object(
        Bucket=DEST_BUCKET,
        Key=new_filename,
        Body=processed_data,
        ContentType="image/jpeg",
        Metadata={
            "processed-via": "flask-imgproxy",
            "processed-timestamp": datetime.now(timezone.utc).isoformat()
        }
    )
    print(f"✅ {key} → {new_filename}")
