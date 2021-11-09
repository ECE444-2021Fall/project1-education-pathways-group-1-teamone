import json
import sys
sys.path.append('../../modules')
from DiscussionTable import DiscussionTable

# Converts the NumLikes field from decimal to string
def convertNumLikesToString(results):
    for comment in results:
        comment["NumLikes"] = str(comment["NumLikes"])

# Handler function called by Lambda
def handler(event, context):
    discussionTable = DiscussionTable()
    params = json.loads(event["body"])

    #Execute the correct action based on the "action" in the parameters
    if params["action"] == "GetComments":
        results = discussionTable.get_item(params["courseID"])["DiscussionBoard"]
        convertNumLikesToString(results)
    elif params["action"] == "AddComment":
        results = discussionTable.add_post(params["courseID"], params["User"], params["DateTime"], params["Message"])
    elif params["action"] == "DeleteComment":
        results = discussionTable.delete_post(params["courseID"], params["PostID"])
    elif params["action"] == "UpvoteComment":
        results = discussionTable.upvote_post(params["courseID"], params["PostID"])
    elif params["action"] == "DownvoteComment":
        results = discussionTable.downvote_post(params["courseID"], params["PostID"])

    headers = { "Content-Type": "application/json" }

    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }
    response['body'] = json.dumps(results)
    return response

# For manual testing purposes
if __name__ == "__main__":
    params1 = {
        "action": "GetComments",
        "courseID": "VPSD57H3"
    }
    params2 = {
        "action": "AddComment",
        "courseID": "VPSD57H3",
        "User": "Griffin Hadfield",
        "DateTime": "10/9/2022 6:43 AM",
        "Message": "This course rocks!"
    }
    params3 = {
        "action": "DeleteComment",
        "courseID": "VPSD57H3",
        "PostID": "f027336d-03b8-4d06-9881-839efcaff2c8"
    }
    params4 = {
        "action": "UpvoteComment",
        "courseID": "VPSD57H3",
        "PostID": "fb5c4992-21a7-494f-b86e-dadce2e9d8c9"
    }
    params5 = {
        "action": "DownvoteComment",
        "courseID": "VPSD57H3",
        "PostID": "fb5c4992-21a7-494f-b86e-dadce2e9d8c9"
    }
    print('\n')
    # print(json.loads(handler({"body": json.dumps(params1)}, {})['body']))
    # json.loads(handler({"body": json.dumps(params2)}, {})['body'])
    # print(json.loads(handler({"body": json.dumps(params3)}, {})['body']))
    print(json.loads(handler({"body": json.dumps(params1)}, {})['body']))
    # print(len(json.loads(handler({"body": json.dumps(params1)}, {})['body'])))