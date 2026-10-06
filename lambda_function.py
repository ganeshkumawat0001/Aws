import json
import boto3
from urllib.parse import unquote_plus

s3 = boto3.client("s3")

RESULT_BUCKET = "ganesh-document-result-2026"


def lambda_handler(event, context):

    print("Received event:", json.dumps(event))

    for record in event.get("Records", []):

        input_bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])

        # Get uploaded file information
        response = s3.head_object(
            Bucket=input_bucket,
            Key=key
        )

        result = {
            "file_name": key.split("/")[-1],
            "file_key": key,
            "file_type": response.get("ContentType", "unknown"),
            "file_size_bytes": response.get("ContentLength", 0),
            "status": "Processed successfully"
        }

        # Create JSON result
        result_key = key + ".json"

        s3.put_object(
            Bucket=RESULT_BUCKET,
            Key=result_key,
            Body=json.dumps(result, indent=2).encode("utf-8"),
            ContentType="application/json"
        )

        print("Result saved:", result_key)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Document processed successfully"
        })
    }
