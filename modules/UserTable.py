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
                "EnrolmentPaths": [],
                "MainPath": ""
            })
            response = self.get_table().put_item(
                Item=params, ConditionExpression='attribute_not_exists(Username)')
        except ClientError as e:  
            if e.response['Error']['Code']=='ConditionalCheckFailedException':  
                response = {
                    "ResponseMetadata": {
                        "HTTPStatusCode": HTTPStatus.CONFLICT
                    }
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
        })
        return response

    # Deletes a user from the database
    def delete_item(self, username):
        response = self.get_table().delete_item(Key={'Username': username})
        return response
