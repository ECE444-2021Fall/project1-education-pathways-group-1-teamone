from Table import Table
from datetime import datetime
import uuid

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
            "Likes": {
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
    def get_item(self, courseID):
            response = self.get_table().get_item(Key={'CourseID': courseID})
            return response['Item']

    def update_item(self):
        #TODO
        pass

    def delete_item(self):
        #TODO
        pass

    def add_post(self, courseID, userName, time, message):
        postID = str(uuid.uuid4())
        newPost = {"PostID": postID, "User": userName, "DateTime": time, "Message": message, "NumLikes": 0}

        self.get_table().update_item(
            Key={'CourseID': courseID},
            UpdateExpression="SET DiscussionBoard = list_append(DiscussionBoard, :i)",
            ExpressionAttributeValues={
                ':i': [newPost],
            },
            ReturnValues="ALL_NEW"
        )
        return newPost

    def get_index_of_post(self, courseID, postID):
        discussionBoard = self.get_item(courseID)["DiscussionBoard"]
        for idx, post in enumerate(discussionBoard):
            if post["PostID"] == postID:
                return idx
        return -1

    def delete_post(self, courseID, postID):
        indexOfPost = self.get_index_of_post(courseID, postID)
        if indexOfPost == -1:
            return "400"

        response = self.get_table().update_item(
            Key={'CourseID': courseID},
            UpdateExpression=f"REMOVE DiscussionBoard[{indexOfPost}]",
            ReturnValues="UPDATED_NEW"
        )
        return response["ResponseMetadata"]["HTTPStatusCode"]

    def upvote_post(self, courseID, postID):
        indexOfPost = self.get_index_of_post(courseID, postID)
        if indexOfPost == -1:
            return "400"
        
        post = self.get_item(courseID)["DiscussionBoard"][indexOfPost]
        post["NumLikes"] += 1

        self.delete_post(courseID, postID)
        response = self.get_table().update_item(
            Key={'CourseID': courseID},
            UpdateExpression="SET DiscussionBoard = list_append(DiscussionBoard, :i)",
            ExpressionAttributeValues={
                ':i': [post],
            },
            ReturnValues="ALL_NEW"
        )
        return str(post["NumLikes"])


    def downvote_post(self, courseID, postID):
        indexOfPost = self.get_index_of_post(courseID, postID)
        if indexOfPost == -1:
            return "400"
        
        post = self.get_item(courseID)["DiscussionBoard"][indexOfPost]
        post["NumLikes"] -= 1

        self.delete_post(courseID, postID)
        response = self.get_table().update_item(
            Key={'CourseID': courseID},
            UpdateExpression="SET DiscussionBoard = list_append(DiscussionBoard, :i)",
            ExpressionAttributeValues={
                ':i': [post],
            },
            ReturnValues="ALL_NEW"
        )
        return str(post["NumLikes"])

if __name__ == "__main__":
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M")
    courseID = "GGR107H1"
    discussion_table = DiscussionTable()
    # print(discussion_table.add_post(courseID, "Griffin Hadfield", date_time, "This course is meh!"))
    # print(discussion_table.delete_post(courseID, "199b4bca-4790-4a4d-8196-7d647995b602"))
    # print(discussion_table.get_item(courseID))
    print(discussion_table.downvote_post(courseID, "d7fce19c-5a07-428c-a080-3416dc194ffe"))