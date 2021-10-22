from botocore.exceptions import ClientError
from Table import Table

# This class implements the ability to add, update, and delete
# courses in the course table in AWS
class CourseTable(Table):
    COURSES_TABLE = "Courses"

    def __init__(self):
        super().__init__(self.COURSES_TABLE)

    # Add the course to the course table with the provided params
    def add_item(self, params):
        response = self.table.put_item(Item=params)

        if response['ResponseMetadata']['HTTPStatusCode'] != 200: 
            print("Error creating course for:", params["CourseID"])
            print(response)
    
    def get_item(self, courseID):
        try:
            response = self.table.get_item(Key={'CourseID': courseID})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']
        
    # Updates an existing course item in the database. Param is the parameter to
    # be updated and value is the value to update it to.
    def update_item(self, courseID, param, value):
        response = self.table.update_item(
        Key={
            'CourseID': courseID,
        },
        UpdateExpression=f"set {param}=:p",
        ExpressionAttributeValues={
            ':p': value,
        })
        return response

    # Deletes a course from the database
    def delete_item(self, courseID):
        response = self.table.delete_item(Key={'CourseID': courseID})
        return response

if __name__ == "__main__":
    course_table = CourseTable()
    course_table.get_item("ECE557H1")
    course_table.update_item("ECE557H1", "Campus", "Canadaaa")
    print(course_table.get_item("ECE557H1"))
