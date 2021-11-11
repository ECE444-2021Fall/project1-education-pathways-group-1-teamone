import json
import hashlib
from UserTable import UserTable
from http import HTTPStatus

def construct_response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value, data={}):
    response = {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False,
        "body": json.dumps(data)
    }
    return response

def attemptLogin(user_table, username, password):
    status = HTTPStatus.UNAUTHORIZED.value
    err_resp = {}
    try:
        user = user_table.get_item(username)
        if user and user['Password'] == password:
            status = HTTPStatus.OK.value
    except Exception as e:
        status = HTTPStatus.BAD_REQUEST.value
        err_resp = {"error_message": str(e)}
    return construct_response(status, err_resp)

# Handler function called by Lambda
def handler(event, context):
    params = json.loads(event["body"])
    
    user_table = UserTable()
    # Route based on preferred action
    action = params['action']
    del params['action']
    if action == "Login":
        return attemptLogin(user_table, params['Username'], params['Password'])
    elif action == "AddUser":
        results = user_table.add_item(params)
    elif action == "GetUser":
        results = user_table.get_item(params['Username'])
    elif action == "DeleteUser":
        results = user_table.delete_item(params['Username'])
    elif action == "AddPath":
        copyPath = params['copyPath'] if 'copyPath' in params else []
        results = user_table.add_enrol_path(
            params['Username'], params['pathName'], copyPath)
    elif action == "GetPath":
        results = user_table.get_enrol_path(params['Username'], params['pathName'])
    elif action == "DeletePath":
        results = user_table.remove_path(params['Username'], params['pathName'])
    elif action == "AddCourse":
        results = user_table.add_course_to_path(
            params['Username'], params['pathName'], params['course'])
    elif action == "RemoveCourse":
        results = user_table.remove_course_from_path(
            params['Username'], params['pathName'], params['courseCode'])

    status = HTTPStatus.INTERNAL_SERVER_ERROR.value
    if not results:
        status = HTTPStatus.INTERNAL_SERVER_ERROR.value    
    elif "HTTPStatusCode" in results:
        status = results["HTTPStatusCode"]
    elif "ResponseMetadata" in results:
        status = results["ResponseMetadata"]["HTTPStatusCode"]
    response = construct_response(status, results)
    return response 

if __name__ == "__main__":
    params = {
        "action": "AddUser",
        "Username": "testUser4",
        "Name": "Test",
        "Email": "test@thisisatest.com",
        "Password": "testpass",
        "Type": "STUDENT",
        "pathName": "path1",
        "courseCode": "TEST121"
    }
    resp = handler({"body": json.dumps(params)}, {})
    print(json.dumps(json.loads(resp['body']), indent=4))
    print(resp['statusCode'])