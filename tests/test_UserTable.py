import pytest
import sys
sys.path.append('./modules')
from modules.UserTable import UserTable, UserTypes

class MockedDynamoTable:
    def put_item(Item=None, ConditionExpression=None):
        response = {
            "ResponseMetadata": {
                "HTTPStatusCode": 200
            }
        }
        return response
    
    def get_item(Key=None):
        response = {
            "Item": {
                "Username": Key["Username"]
            }
        }
        return response

    def update_item(Key=None, UpdateExpression=None, ExpressionAttributeValues=None):
        response = {
            "ResponseMetadata": {
                "HTTPStatusCode": 200
            }
        }
        return response
    
    def delete_item(Key=None):
        response = {
            "ResponseMetadata": {
                "HTTPStatusCode": 200
            }
        }
        return response

@pytest.fixture     
def mocked_get_table():
    return MockedDynamoTable

def test_add_item(mocker, mocked_get_table):
    mocker.patch('modules.UserTable.UserTable.get_table', return_value=MockedDynamoTable)
    user_table = UserTable()

    put_item_spy = mocker.spy(mocked_get_table, 'put_item')

    params = {
        "Username" : "testUser",
        "Name": "Test",
        "Email": "test@thisisatest.com",
        "Password": "testpass",
        "Type": str(UserTypes.STUDENT_TYPE)
    }
    params_complete = params.copy().update({
        "Active": True,
        "EnrolmentPaths": [],
        "MainPath": ""
    })
    response = user_table.add_item(params)
    put_item_spy.assert_called_once_with(Item=params, ConditionExpression='attribute_not_exists(Username)')
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
    

def test_get_item(mocker, mocked_get_table):
    mocker.patch('modules.UserTable.UserTable.get_table', return_value=MockedDynamoTable)
    user_table = UserTable()

    get_item_spy = mocker.spy(mocked_get_table, 'get_item')

    username = "testUser"
    response = user_table.get_item(username)

    get_item_spy.assert_called_once_with(Key={'Username': username})
    assert response == {"Username":"testUser"}

def test_update_item(mocker, mocked_get_table):
    mocker.patch('modules.UserTable.UserTable.get_table', return_value=MockedDynamoTable)
    user_table = UserTable()

    update_item_spy = mocker.spy(mocked_get_table, 'update_item')

    username = "testUser"
    param = "Email"
    updated_value = "nowaitthisismyemail@test.com"
    
    response = user_table.update_item(username, param, updated_value)

    update_item_spy.assert_called_once_with(Key={
            'Username': username,
        },
        UpdateExpression=f"set {param}=:p",
        ExpressionAttributeValues={
            ':p': updated_value,
        })
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

def test_delete_item(mocker, mocked_get_table):
    mocker.patch('modules.UserTable.UserTable.get_table', return_value=MockedDynamoTable)
    user_table = UserTable()

    get_item_spy = mocker.spy(mocked_get_table, 'delete_item')

    username = "testUser"
    response = user_table.delete_item(username)

    get_item_spy.assert_called_once_with(Key={'Username': username})
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

