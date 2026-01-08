import json
import boto3
import uuid

s3 = boto3.client("s3")

BUCKET_NAME = "image-label-generator-burkul"  # <-- YOUR UPLOAD BUCKET

def lambda_handler(event, context):
    try:
        params = event.get("queryStringParameters") or {}
        file_name = params.get("file_name")

        if not file_name:
            return {
                "statusCode": 400,
                "headers": cors_headers(),
                "body": json.dumps({"error": "file_name is required"})
            }

        unique_name = f"{uuid.uuid4()}_{file_name}"

        upload_url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": unique_name,
                "ContentType": "image/jpeg"
            },
            ExpiresIn=300
        )

        return {
            "statusCode": 200,
            "headers": cors_headers(),
            "body": json.dumps({
                "upload_url": upload_url,
                "image_name": unique_name
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": cors_headers(),
            "body": json.dumps({"error": str(e)})
        }


def cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "GET,OPTIONS"
    }
