import boto3

boto3.setup_default_session(profile_name='444')

# This class implements the functionality nessecary to upload a course and 
# a discssion board to the associated tables in AWS 
class CourseImporter:
    COURSES_TABLE = "Courses"
    DISCUSSION_BOARD_TABLE = "CourseDiscussionBoards"

    def __init__(self):
        # AWS Configuartion 
        self.endpoint_url = "https://dynamodb.us-east-1.amazonaws.com"
        self.dynamodb = boto3.resource('dynamodb', endpoint_url=self.endpoint_url)
        self.courses_table = self.dynamodb.Table(CourseImporter.COURSES_TABLE)
        self.discussion_table = self.dynamodb.Table(CourseImporter.DISCUSSION_BOARD_TABLE)

    # Given the course information in params, add the course to the course_table and 
    # add an associated discussion board to the discussion_table
    def create_course(self, params):
        courseTableItem = params
        discussionTableItem = {
            "Ratings": {
                "Homework": 0,
                "Content": 0,
                "Exams": 0
            },
            "DiscussionBoard": []
        }        
        discussionTableItem['CourseID'] = params['CourseID']
        
        response1 = self.courses_table.put_item(Item=courseTableItem)
        response2 = self.discussion_table.put_item(Item=discussionTableItem)

        if response1['ResponseMetadata']['HTTPStatusCode'] != 200: 
            print("Error creating course for:", params["CourseID"])
            print(response1) 

        if response2['ResponseMetadata']['HTTPStatusCode'] != 200: 
            print("Error creating discussion board for:", params["CourseID"])
            print(response2)
