from Table import Table

# This class implements the ability to add and modify discussion boards in 
# the discussion table in AWS
class DiscussionTable(Table):
    DISCUSSION_BOARD_TABLE = "CourseDiscussionBoards"

    def __init__(self):
        super().__init__(self.DISCUSSION_BOARD_TABLE)

    def get_table(self):
        return self.table

    # Add an empty discussion board to the table with the provided courseID
    def add_item(self, courseID):
        discussionTableItem = {
            "CourseID": courseID,
            "Ratings": {
                "Homework": 0,
                "Content": 0,
                "Exams": 0
            },
            "DiscussionBoard": []
        }        

        response = self.table.put_item(Item=discussionTableItem)

        if response['ResponseMetadata']['HTTPStatusCode'] != 200: 
            print("Error creating discussion board for:", courseID)
            print(response)
    def get_item(self):
        #TODO
        pass

    def update_item(self):
        #TODO
        pass

    def delete_item(self):
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