import boto3
from botocore.exceptions import ClientError

boto3.setup_default_session(profile_name='444')

# This class implements the ability to add, update, and delete
# courses in the course table in AWS
class CourseTable:
    COURSES_TABLE = "Courses"
    DISCUSSION_BOARD_TABLE = "CourseDiscussionBoards"

    def __init__(self):
        # AWS Configuartion 
        self.endpoint_url = "https://dynamodb.us-east-1.amazonaws.com"
        self.dynamodb = boto3.resource('dynamodb', endpoint_url=self.endpoint_url)
        self.courses_table = self.dynamodb.Table(CourseTable.COURSES_TABLE)

    # Given the course information in params, add the course to the course_table and 
    def add_course(self, params):
        response = self.courses_table.put_item(Item=params)

        if response['ResponseMetadata']['HTTPStatusCode'] != 200: 
            print("Error creating course for:", params["CourseID"])
            print(response)
    
    def get_course(self, courseID):
        try:
            response = self.courses_table.get_item(Key={'CourseID': courseID})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']
        
    # Updates an existing course item in the database
    def update_course(self, courseID, param, value):
        response = self.courses_table.update_item(
        Key={
            'CourseID': courseID,
        },
        UpdateExpression=f"set {param}=:p",
        ExpressionAttributeValues={
            ':p': value,
        })
        return response

    # Updates an existing course item in the database
    def delete_course(self, courseID):
        response = self.courses_table.delete_item(Key={'CourseID': courseID})
        return response

# if __name__ == "__main__":
#     course_table = CourseTable()
#     course_table.get_course("CLA101H5")
#     course_table.update_course("CLA101H5", "Campus", "Dubai")
#     course_table.get_course("CLA101H5")
#     course_table.delete_course("CLA101H5")
