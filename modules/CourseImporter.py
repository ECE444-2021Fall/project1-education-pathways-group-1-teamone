import boto3


boto3.setup_default_session(profile_name='444')

class CourseImporter:
    COURSES_TABLE = "Courses"
    DISCUSSION_BOARD_TABLE = "CourseDiscussionBoards"
    
    COURSE_TABLE_PARAMS = set([
        "CourseID",
        "Name",
        "Division",
        "Description",
        "Department",
        "Level",
        "Campus",
        "Prerequisites",
        "Term",
        "MajorOutcomes",
        "MinorOutcomes"
    ])

    DISCUSSION_BOARD_TABLE_PARAMS = set([
        "CourseID",
        "Ratings",
        "DiscussionBoard"
    ])

    def __init__(self):
        self.endpoint_url = "https://dynamodb.us-east-1.amazonaws.com"
        self.dynamodb = boto3.resource('dynamodb', endpoint_url=self.endpoint_url)
        self.courses_table = self.dynamodb.Table(CourseImporter.COURSES_TABLE)
        self.discussion_table = self.dynamodb.Table(CourseImporter.DISCUSSION_BOARD_TABLE)

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
    
if __name__ == "__main__":
    importer = CourseImporter()
    importer.create_course({
        "CourseID": "TEST444",
        "Name": "TEST COURSE",
        "Division": "THE FRAT",
        "Description": "TESTING",
        "Department": "OKE",
        "Level": 0
    })
