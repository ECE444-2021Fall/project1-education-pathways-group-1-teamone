import pytest
import sys
sys.path.append('../modules')
from modules.CourseTable import CourseTable

class MockedDynamoTable:
    def put_item(Item=None):
        response = {
            "ResponseMetadata": {
                "HTTPStatusCode": 200
            }
        }
        return response
    
    def get_item(Key=None):
        response = {
            "Item": {
                "CourseID": Key["CourseID"]
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
    
    mocker.patch('modules.CourseTable.CourseTable.get_table', return_value=MockedDynamoTable)
    course_table = CourseTable()

    put_item_spy = mocker.spy(mocked_get_table, 'put_item')

    params = {"CourseID":"ECE444H1"}
    response = course_table.add_item(params)
    put_item_spy.assert_called_once_with(Item=params)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
    

def test_get_item(mocker, mocked_get_table):
    mocker.patch('modules.CourseTable.CourseTable.get_table', return_value=MockedDynamoTable)
    course_table = CourseTable()

    get_item_spy = mocker.spy(mocked_get_table, 'get_item')

    courseID = "ECE444H1"
    response = course_table.get_item(courseID)

    get_item_spy.assert_called_once_with(Key={'CourseID': courseID})
    assert response == {"CourseID":"ECE444H1"}

def test_update_item(mocker, mocked_get_table):
    mocker.patch('modules.CourseTable.CourseTable.get_table', return_value=MockedDynamoTable)
    course_table = CourseTable()

    update_item_spy = mocker.spy(mocked_get_table, 'update_item')

    courseID = "ECE444H1"
    param = "Description"
    updated_value = "This course rocks"
    
    response = course_table.update_item(courseID, param, updated_value)

    update_item_spy.assert_called_once_with(Key={
            'CourseID': courseID,
        },
        UpdateExpression=f"set {param}=:p",
        ExpressionAttributeValues={
            ':p': updated_value,
        })
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

def test_delete_item(mocker, mocked_get_table):
    mocker.patch('modules.CourseTable.CourseTable.get_table', return_value=MockedDynamoTable)
    course_table = CourseTable()

    get_item_spy = mocker.spy(mocked_get_table, 'delete_item')

    courseID = "ECE444H1"
    response = course_table.delete_item(courseID)

    get_item_spy.assert_called_once_with(Key={'CourseID': courseID})
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200