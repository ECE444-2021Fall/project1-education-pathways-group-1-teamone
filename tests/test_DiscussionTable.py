import pytest
import sys
sys.path.append('../modules')
from modules.DiscussionTable import DiscussionTable

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
                "CourseID": Key["CourseID"],
                "DiscussionBoard": [{"PostID": "fake-id", "message": "This course rocks!", "NumLikes": 0}]
            }
        }
        return response

    def update_item(Key=None, UpdateExpression=None, ExpressionAttributeValues=None, ReturnValues=None):
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
    
    mocker.patch('modules.DiscussionTable.DiscussionTable.get_table', return_value=MockedDynamoTable)
    discussion_table = DiscussionTable()

    put_item_spy = mocker.spy(mocked_get_table, 'put_item')

    courseID = "ECE444H1"
    response = discussion_table.add_item(courseID)
    put_item_spy.assert_called_once_with(Item={
            "CourseID": courseID,
            "DiscussionBoard": []
        })
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
    
def test_get_item(mocker, mocked_get_table):
    mocker.patch('modules.DiscussionTable.DiscussionTable.get_table', return_value=MockedDynamoTable)
    discussion_table = DiscussionTable()

    get_item_spy = mocker.spy(mocked_get_table, 'get_item')

    courseID = "ECE444H1"
    response = discussion_table.get_item(courseID)

    get_item_spy.assert_called_once_with(Key={'CourseID': courseID})
    assert response == {
                "CourseID": courseID,
                "DiscussionBoard": [{"PostID": "fake-id", "message": "This course rocks!", "NumLikes": 0}]
            }

def test_update_item(mocker, mocked_get_table):
    mocker.patch('modules.DiscussionTable.DiscussionTable.get_table', return_value=MockedDynamoTable)
    discussion_table = DiscussionTable()

    update_item_spy = mocker.spy(mocked_get_table, 'update_item')

    courseID = "ECE444H1"
    param = "Description"
    updated_value = "This course rocks"
    
    response = discussion_table.update_item(courseID, param, updated_value)

    update_item_spy.assert_called_once_with(Key={
            'CourseID': courseID,
        },
        UpdateExpression=f"set {param}=:p",
        ExpressionAttributeValues={
            ':p': updated_value,
        })
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

def test_delete_item(mocker, mocked_get_table):
    mocker.patch('modules.DiscussionTable.DiscussionTable.get_table', return_value=MockedDynamoTable)
    discussion_table = DiscussionTable()

    get_item_spy = mocker.spy(mocked_get_table, 'delete_item')

    courseID = "ECE444H1"
    response = discussion_table.delete_item(courseID)

    get_item_spy.assert_called_once_with(Key={'CourseID': courseID})
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

def test_add_post(mocker, mocked_get_table):
    mocker.patch('modules.DiscussionTable.DiscussionTable.get_table', return_value=MockedDynamoTable)
    discussion_table = DiscussionTable()

    update_item_spy = mocker.spy(mocked_get_table, 'update_item')

    courseID = "ECE444H1"
    userName = "Griffin Hadfield"
    time = "10/09/2021 6:34AM"
    message = "This course rocks!"

    response = discussion_table.add_post(courseID, userName, time, message)

    postID = response["PostID"]
    newPost = {"PostID": postID, "User": userName, "DateTime": time, "Message": message, "NumLikes": 0}

    update_item_spy.assert_called_once_with(
            Key={'CourseID': courseID},
            UpdateExpression="SET DiscussionBoard = list_append(DiscussionBoard, :i)",
            ExpressionAttributeValues={
                ':i': [newPost],
            },
            ReturnValues="ALL_NEW")
    assert response == newPost

def test_delete_post(mocker, mocked_get_table):
    mocker.patch('modules.DiscussionTable.DiscussionTable.get_table', return_value=MockedDynamoTable)
    discussion_table = DiscussionTable()

    update_item_spy = mocker.spy(mocked_get_table, 'update_item')

    courseID = "ECE444H1"
    postID = "fake-id"
    response = discussion_table.delete_post(courseID, postID)

    update_item_spy.assert_called_once_with(
            Key={'CourseID': courseID},
            UpdateExpression="REMOVE DiscussionBoard[0]",
            ReturnValues="UPDATED_NEW"
            )
    assert response == 200

def test_upvote_post(mocker, mocked_get_table):
    mocker.patch('modules.DiscussionTable.DiscussionTable.get_table', return_value=MockedDynamoTable)
    discussion_table = DiscussionTable()

    update_item_spy = mocker.spy(mocked_get_table, 'update_item')

    courseID = "ECE444H1"
    postID = "fake-id"
    response = discussion_table.upvote_post(courseID, postID)

    post = {"PostID": "fake-id", "message": "This course rocks!", "NumLikes": 1}

    update_item_spy.assert_any_call(
            Key={'CourseID': courseID},
            UpdateExpression="SET DiscussionBoard = list_append(DiscussionBoard, :i)",
            ExpressionAttributeValues={
                ':i': [post],
            },
            ReturnValues="ALL_NEW"
        )
    assert response == '1'

def test_downvote_post(mocker, mocked_get_table):
    mocker.patch('modules.DiscussionTable.DiscussionTable.get_table', return_value=MockedDynamoTable)
    discussion_table = DiscussionTable()

    update_item_spy = mocker.spy(mocked_get_table, 'update_item')

    courseID = "ECE444H1"
    postID = "fake-id"
    response = discussion_table.downvote_post(courseID, postID)

    post = {"PostID": "fake-id", "message": "This course rocks!", "NumLikes": -1}

    update_item_spy.assert_any_call(
            Key={'CourseID': courseID},
            UpdateExpression="SET DiscussionBoard = list_append(DiscussionBoard, :i)",
            ExpressionAttributeValues={
                ':i': [post],
            },
            ReturnValues="ALL_NEW"
        )
    assert response == '-1'

