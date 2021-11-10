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