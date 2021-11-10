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

# Converts the DynamoDB formatted values of a field to a list of strings.
# So that it is easier to work with. 
# For example, if the fieldName is "Prerequisites" with a value of:
#   {'L': [{'S': 'PPGB66H3'}, {'S': 'POLB50Y3'}, {'S': 'POLB92H3'}]}
# This function would return ['PPGB66H3', 'POLB50Y3', 'POLB92H3']
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

# Reformat the results into the following format:
# { "<CourseID>" : {
#     "score": "<score>"
#     "data": {
#         "name": ["<name>"],
#         "prerequsites": ["<prereq1>, <prereq2>"],
#         ...
#     },
#
#  "<CourseID>": {...},
#   ...
# }}
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

# Remove results that don't match the filter.
# This function doesn't return anthing, the results parameter
# is modified directly.
def filter_results(results, filters):
    coursesToRemove = set()
    for courseID, course in results.items():
        for fieldName, values in course["data"].items():
            matchFound = False
            for val in values:
                if fieldName in filters and val in filters[fieldName]:
                    matchFound = True
            if fieldName in filters and not matchFound:
                coursesToRemove.add(courseID)
    for courseID in coursesToRemove:
        del results[courseID]      

# Handler function called by Lambda
def handler(event, context):
    # Construct the query object based on the search parameters
    params = json.loads(event["body"])
    query = {
        "from": params["from"] if "from" in params else 0,
        "size": params["numResults"] if "numResults" in params else 20,
            }
    # If a query string is present, search using that string
    if params["queryString"]:
        query["query"] = {
                    "multi_match": {
                        "query": params['queryString'],
                        "fields": ["CourseID.S^4", "Name.S^3", "Description.S^2", "Division.S", "Department.S"]
                    },
                }
    else:
        # If now query is present, we can simply match and return all results
        query["query"] = {"match_all": {}}

    headers = { "Content-Type": "application/json" }

    # Make the signed HTTP request
    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
    if r.status_code != 200:
        return r.text

    # Create the response and add some extra content to support CORS
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }

    # Format and filter the results
    unformattedResults = json.loads(r.text)['hits']['hits']
    formattedResults = format_results(unformattedResults)
    filter_results(formattedResults, params['filters'] if "filters" in params else {})

    # Add the search results to the response
    response['body'] = json.dumps(formattedResults)
    return response

if __name__ == "__main__":
    params = {
        "from": 0,
        "numResults": 10,
        "queryString": "science", 
        "filters": {
            "Division": ["University of Toronto Scarborough"],
            "Level": ["1", "4"]
        }
    }
    print(json.dumps(json.loads(handler({"body": json.dumps(params)}, {})['body']), indent=4))