import boto3

boto3.setup_default_session(profile_name='444')

# This class implements the ability to add and modify discussion board in 
# the discussion table in AWS
class DiscussionTable:
    DISCUSSION_BOARD_TABLE = "CourseDiscussionBoards"

    def __init__(self):
        # AWS Configuartion 
        self.endpoint_url = "https://dynamodb.us-east-1.amazonaws.com"
        self.dynamodb = boto3.resource('dynamodb', endpoint_url=self.endpoint_url)
        self.discussion_table = self.dynamodb.Table(DiscussionTable.DISCUSSION_BOARD_TABLE)

    # Given the course information in params, add the course to the course_table and 
    # add an associated discussion board to the discussion_table
    def add_discussion_board(self, courseID):
        discussionTableItem = {
            "CourseID": courseID,
            "Ratings": {
                "Homework": 0,
                "Content": 0,
                "Exams": 0
            },
            "DiscussionBoard": []
        }        

        response = self.discussion_table.put_item(Item=discussionTableItem)

        if response['ResponseMetadata']['HTTPStatusCode'] != 200: 
            print("Error creating discussion board for:", courseID)
            print(response)

    def update_course_rating(self):
        #TODO
        pass
    
    def add_post(self):
        #TODO
        pass

    def remove_post(self):
        #TODO
        pass

    def upvote_post(self):
        #TODO
        pass

    def downvote_post(self):
        #TODO
        pass