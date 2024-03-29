import json
import boto3

# Assuming the use of CloudFront
cloudfront_domain_name = 'yourCloudFrontDomainName.cloudfront.net'

def get_asset_group_url(event, context):
    # Extracting the group name from the query parameters
    params = event.get('queryStringParameters', {})
    group_name = params.get('groupName', None)
    
    if not group_name:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({"error": "GroupName query parameter is required"})
        }

    # Generate the base URL for the asset group
    base_url = f"https://{cloudfront_domain_name}/{group_name}/"

    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
        "body": json.dumps({
            "message": "URL retrieved successfully",
            "url": base_url
        })
    }
