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

        # Construct the URL for the new 'directory'
        bucket_location = s3_client.get_bucket_location(Bucket="asset-manager-server-bucket")
        region = bucket_location['LocationConstraint']
        url = f"https://{region}.amazonaws.com/asset-manager-server-bucket/{directory_name}"

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Asset group created successfully!",
                "directoryUrl": url
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
