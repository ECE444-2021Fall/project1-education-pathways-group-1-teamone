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

STRING_FIELDS = ["CourseID", "Description", "Division", "Campus", "Department", "Name"]
NUM_FIELDS = ["Level"]
LIST_FIELDS = ["MinorOutcomes", "MajorOutcomes", "Term", "Prerequisites"]

def convertFieldValueToList(fieldName, value):
    valuesList = []
    if fieldName in STRING_FIELDS:
        valuesList.append(value["S"])
    elif fieldName in NUM_FIELDS:
        valuesList.append(value["N"])
    elif fieldName in LIST_FIELDS:
        for val in value["L"]:
            valuesList.append(val["S"])
    return valuesList

def format_results(results):
    formattedResults = {}
    for result in results:
        courseResult = {
            "data": {},
            "score": result["_score"]
        }
        for fieldName, values in result["_source"].items():
            courseResult["data"][fieldName] = convertFieldValueToList(fieldName, values)
        
        courseID = result["_source"]["CourseID"]["S"]
        formattedResults[courseID] = courseResult

    return formattedResults

def filter_results(results, filters):
    coursesToRemove = set()
    for courseID, course in results.items():
        for fieldName, values in course["data"].items():
            for val in values:
                if fieldName in filters and val not in filters[fieldName]:
                    coursesToRemove.add(courseID)
    print("REMOVING", len(coursesToRemove))
    for courseID in coursesToRemove:
        del results[courseID]      

def lambda_handler(event, context):

    query = {
        "from": event["from"] if "from" in event else 0,
        "size": event["numResults"] if "numResults" in event else 20,
        "query": {
                    "multi_match": {
                        "query": event['queryString'],
                        "fields": ["CourseID.S^4", "Name.S^3", "Description.S^2", "Division.S", "Department.S"]
                    },
                },
            }

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

    unformattedResults = json.loads(r.text)['hits']['hits']
    formattedResults = format_results(unformattedResults)
    filter_results(formattedResults, event['filters'] if "filters" in event else {})
    print(len(formattedResults.keys()), formattedResults.keys())

    # Add the search results to the response
    response['body'] = json.dumps(formattedResults)
    return response

if __name__ == "__main__":
    event = {
        "from": 0,
        "numResults": 5,
        "queryString": "science", 
        "filters": {
            "Division": ["University of Toronto Scarborough"],
            "Level": ["1", "4"]
        }
    }
    
    json.dumps(json.loads(lambda_handler(event, {})['body']), indent=4)