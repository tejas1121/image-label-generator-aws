import boto3
import json
from decimal import Decimal
from datetime import datetime

# Initialize AWS clients
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ImageLabels')  # Correct table name

def lambda_handler(event, context):
    # Check if event is from S3
    if 'Records' not in event:
        return {"statusCode": 400, "body": "No S3 Records found in event"}
    
    # Extract bucket and object key
    record = event['Records'][0]['s3']
    bucket = record['bucket']['name']
    image_name = record['object']['key']
    
    print(f"Processing image: {image_name} from bucket: {bucket}")
    
    try:
        # Call Rekognition to detect labels
        response = rekognition.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': image_name}},
            MaxLabels=50,
            MinConfidence=70  # Rekognition filtering
        )
        
        labels = response['Labels']
        print(f"Detected labels: {labels}")
        
        # Filter labels with confidence >= 90%
        filtered_labels = [
            {"Name": label['Name'], "Confidence": str(label['Confidence'])}
            for label in labels
            if label['Confidence'] >= 90
        ]
        
        # Prepare item for DynamoDB
        item = {
            'image_name': image_name,
            'Labels': filtered_labels,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Store in DynamoDB
        table.put_item(Item=item)
        print("Successfully stored labels in DynamoDB")
        
        return {
            "statusCode": 200,
            "body": json.dumps(item)
        }
        
    except Exception as e:
        print(f"Error processing image {image_name}: {str(e)}")
        return {"statusCode": 500, "body": str(e)}
