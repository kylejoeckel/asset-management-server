import json
import uuid
import boto3

s3_client = boto3.client('s3')

def create_asset_group(event, context):
    try:
        # Parse the request body
        body = json.loads(event.get('body', '{}'))
        asset_group_name = body.get('assetGroupName')

        # Generate a unique ID for the asset group
        unique_id = str(uuid.uuid4())
        directory_name = f"{asset_group_name}-{unique_id}/"

        # Creating the 'directory' (no content needed, just the key)
        s3_client.put_object(Bucket="asset-manager-server-bucket", Key=directory_name)

        # Construct the URL for the new 'directory' using virtual-hosted-style URL
        url = f"https://asset-manager-server-bucket.s3.amazonaws.com/{directory_name}"

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({
                "message": "Asset group created successfully!",
                "directoryUrl": url
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({"error": str(e)})
        }
