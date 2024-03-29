import json
import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
bucket_name = 'asset-manager-server-bucket'  # Your S3 bucket name
cloudfront_domain_name = 'yourCloudFrontDomainName.cloudfront.net'  # Your CloudFront domain

def add_asset_to_group(event, context):
    try:
        body = json.loads(event['body'])
        group_name = body.get('groupName')
        asset_name = body.get('assetName')
        
        if not all([group_name, asset_name]):
            return {
                "statusCode": 400,
                "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
                "body": json.dumps({"error": "GroupName and AssetName are required"})
            }
        
        # Generate the S3 key for the asset
        s3_key = f"{group_name}/{asset_name}"

        # Generate a pre-signed URL for uploading
        presigned_url = s3_client.generate_presigned_url('put_object', 
                                                         Params={'Bucket': bucket_name, 'Key': s3_key},
                                                         ExpiresIn=3600)  # URL expires in 1 hour

        # Generate the CDN URL for accessing the uploaded asset
        asset_url = f"https://{cloudfront_domain_name}/{s3_key}"

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({
                "message": "Pre-signed URL generated successfully",
                "presignedUrl": presigned_url,
                "assetUrl": asset_url
            })
        }
    except ClientError as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({"error": str(e)})
        }
