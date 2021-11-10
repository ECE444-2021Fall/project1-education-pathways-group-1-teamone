from botocore.exceptions import ClientError
from enum import Enum
from http import HTTPStatus
from Table import Table

class UserTypes(Enum):
    STUDENT_TYPE = "STUDENT"
    ADMIN_TYPE = "ADMIN"
    OTHER_TYPE = "OTHER"


# This class implements the ability to add, update, and delete
# users in the user table in AWS
class UserTable(Table):
    USERS_TABLE = "Users"

    def __init__(self):
        super().__init__(self.USERS_TABLE)

    def get_table(self):
        return self.table

    # Add the user to the user table with the provided params IF the user does not exist
    def add_item(self, params):
        try:
            params.update({
                "Active": True,
                "EnrolmentPaths": {},
                "MainPath": ""
            })
            response = self.get_table().put_item(
                Item=params, ConditionExpression='attribute_not_exists(Username)')
        except ClientError as e:  
            if e.response['Error']['Code']=='ConditionalCheckFailedException':  
                response = {
                    "ResponseMetadata": {
                        "HTTPStatusCode": HTTPStatus.CONFLICT
                    },
                    "HTTPStatusCode": HTTPStatus.CONFLICT
                }
        else:
            if response['ResponseMetadata']['HTTPStatusCode'] != HTTPStatus.OK: 
                print("Error creating user for:", params["Username"])
                print(response)
            return response

    def get_item(self, username):
        try:
            response = self.get_table().get_item(Key={'Username': username})
            print(response)
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise(ClientError)
        else:
            return response['Item'] if 'Item' in response else {}
        
    # Updates an existing user item in the database. Param is the parameter to
    # be updated and value is the value to update it to.
    def update_item(self, username, param, value):
        response = self.get_table().update_item(
            Key={
                'Username': username,
            },
            UpdateExpression=f"set {param}=:p",
            ExpressionAttributeValues={
                ':p': value,
            }
        )
        return response

    # Deletes a user from the database
    def delete_item(self, username):
        response = self.get_table().delete_item(Key={'Username': username})
        return response

    # Adds an enrolment path to the given user, if dupe_from is not empty/None,
    # the path will be a duplicate of dupe_from
    def add_enrol_path(self, username, path_name, dupe_from=[]):
        return self.get_table().update_item(
            Key={'Username': username},
            UpdateExpression="SET EnrolmentPaths.#pname = :i",
            ExpressionAttributeNames={
                '#pname': path_name
            },
            ExpressionAttributeValues={
                ':i': dupe_from,
            },
            ReturnValues="ALL_NEW"
        )

    # Gets a specific enrolment path for a given user.
    # Returns HTTP status NOT_FOUND if the path does not exist
    def get_enrol_path(self, username, path_name):
        user_obj = self.get_item(username)
        status = HTTPStatus.OK
        data = {}
        if 'EnrolmentPaths' not in user_obj and path_name not in user_obj['EnrolmentPaths']:
            status = HTTPStatus.NOT_FOUND
        else:
            data = user_obj['EnrolmentPaths'][path_name]
        return {
            **data,
            "ResponseMetadata": {
                "HTTPStatusCode": status
            },
            "HTTPStatusCode": status
        }
    
    # Remove a specific enrolment path for a given user
    def remove_path(self, username, path_name):
        status = HTTPStatus.OK
        if self.get_enrol_path(username, path_name)["HTTPStatusCode"] == HTTPStatus.NOT_FOUND:
            status = HTTPStatus.NOT_FOUND
        else:
            response = self.get_table().update_item(
                Key={'Username': username},
                UpdateExpression=f"REMOVE EnrolmentPaths.{path_name}",
                ReturnValues="UPDATED_NEW"
            )
            status = response["ResponseMetadata"]["HTTPStatusCode"]
        return {
            "ResponseMetadata": {
                "HTTPStatusCode": status
            },
            "HTTPStatusCode": status
        }
    
    # Add a course to a specific path.
    # Example course: 
    # {
    #   "Code": "ECE444",
    #   "Name": "Software Engineering",
    #   "Semester": "2021 Fall"
    # }
    # **** Note that the only REQUIRED attribute in the course object is the Code ****
    def add_course_to_path(self, username, path_name, course):
        status = HTTPStatus.OK
        resp = None
        if self.get_enrol_path(username, path_name)["HTTPStatusCode"] == HTTPStatus.NOT_FOUND:
            status = HTTPStatus.BAD_REQUEST
        else:
            attr = f"EnrolmentPaths.{path_name}"
            resp = self.get_table().update_item(
                Key={'Username': username},
                UpdateExpression=f"SET {attr} = list_append({attr}, :i)",
                ExpressionAttributeValues={
                    ':i': [course],
                },
                ReturnValues="ALL_NEW"
            )
        return resp or {
            "ResponseMetadata": {
                "HTTPStatusCode": status
            },
            "HTTPStatusCode": status
        }
    
    # Given a course code and enrolment path, find the index of the course in the path list
    def get_index_of_course(self, username, path_name, course_code):
        path = self.get_enrol_path(username, path_name)
        for idx, course in enumerate(path):
            if course["Code"] == course_code:
                return idx
        return -1

    # Given a course code and enrolment path, remove the course from the path list
    def remove_course_from_path(self, username, path_name, course_code):
        status = HTTPStatus.BAD_REQUEST
        resp = None
        if self.get_enrol_path(username, path_name)["HTTPStatusCode"] != HTTPStatus.NOT_FOUND:
            index = self.get_index_of_course(username, path_name, course_code)
            if index != -1:
                attr = f"EnrolmentPaths.{path_name}[{index}]"
                resp = self.get_table().update_item(
                    Key={'Username': username},
                    UpdateExpression=f"REMOVE {attr}",
                    ReturnValues="UPDATED_NEW"
                )
        return resp or {
            "ResponseMetadata": {
                "HTTPStatusCode": status
            },
            "HTTPStatusCode": status
        }