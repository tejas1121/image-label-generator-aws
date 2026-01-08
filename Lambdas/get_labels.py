import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("ImageLabels")

def lambda_handler(event, context):
    params = event.get("queryStringParameters") or {}
    image_name = params.get("image_name")

    # ❌ only return 400 if parameter is missing
    if not image_name:
        return response(400, {"error": "image_name is required"})

    result = table.get_item(Key={"image_name": image_name})

    # ⏳ labels not ready yet
    if "Item" not in result:
        return response(404, {"status": "processing"})

    # ✅ labels ready
    return response(200, result["Item"])


def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS"
        },
        "body": json.dumps(body)
    }
