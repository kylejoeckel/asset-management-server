import json
import boto3

s3_client = boto3.client('s3')

def list_menu_assets(event, context):
    try:
        # Parse the query parameters
        query_params = event.get('queryStringParameters', {})
        asset_group_name = query_params.get('groupName')

        if not asset_group_name:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True,
                },
                "body": json.dumps({"error": "groupName parameter is required"})
            }

        # Define the bucket name
        bucket_name = "asset-manager-server-bucket"

        # Define valid image extensions (excluding PDF)
        valid_extensions = ['.pdf']

        # Initialize the list of assets
        assets = []

        # List objects in the bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=asset_group_name + "-")

        # Filter objects by valid image extensions
        for item in response.get('Contents', []):
            file_name = item['Key'].split('/')[-1]  # Extract file name
            file_extension = '.' + file_name.split('.')[-1].lower() if '.' in file_name else ''
            
            if file_extension in valid_extensions:
                # Append the asset to the list with the required format
                assets.append('/' + file_name)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps(assets)
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
