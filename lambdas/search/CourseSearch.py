import boto3
import requests
import json
from requests_aws4auth import AWS4Auth

region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://search-courses-nb4cbsmwocu5uvwtwhxdcvkeha.us-east-1.es.amazonaws.com'
index = 'lambda-index'
url = host + '/' + index + '/_search'

# Lambda execution starts here
TEST_QUERY = "computer engineering"
def lambda_handler(event, context):

    # Put the user query into the query DSL for more accurate search results.
    # Note that certain fields are boosted (^).
    query = {
        "size": 50,
        "query": {
            "multi_match": {
                "query": TEST_QUERY if not event else event['queryStringParameters']['q']
            }
        }
    }

    # Elasticsearch 6.x requires an explicit Content-Type header
    headers = { "Content-Type": "application/json" }

    # Make the signed HTTP request
    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))

    # Create the response and add some extra content to support CORS
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }

    # Add the search results to the response
    response['body'] = r.text
    return response

if __name__ == "__main__":
    print(json.dumps(json.loads(lambda_handler({}, {})['body']), indent=4))
    print(len(json.loads(lambda_handler({}, {})['body'])['hits']['hits']))
    # print(type(lambda_handler({}, {})['body']))