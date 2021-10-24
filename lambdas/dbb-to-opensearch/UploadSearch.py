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
type = '_doc'
url = host + '/' + index + '/' + type + '/'

headers = { "Content-Type": "application/json" }

def handler(event, context):
    count = 0
    try:
        # print("Input:")
        # print(json.dumps(event))
        for record in event['Records']:
            # Get the primary key for use as the OpenSearch ID
            id = record['dynamodb']['Keys']['CourseID']['S']
            r = None
            if record['eventName'] == 'REMOVE':
                r = requests.delete(url + id, auth=awsauth)
            else:
                document = record['dynamodb']['NewImage']
                r = requests.put(url + id, auth=awsauth, json=document, headers=headers)
            if r.status_code != 200 or r.status_code != 201:
                print("Response:")
                print(r)
            count += 1
    except Exception as e:
        print(e)
        raise e
    return str(count) + ' records processed.'