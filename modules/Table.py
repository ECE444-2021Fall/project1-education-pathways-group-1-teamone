from abc import ABC, abstractmethod
import boto3


# Abstract base class for dynamoDB table in AWS
class Table(ABC):

    def __init__(self, table_name):
        # AWS Configuartion 
        self.endpoint_url = "https://dynamodb.us-east-1.amazonaws.com"
        self.dynamodb = boto3.resource('dynamodb', endpoint_url=self.endpoint_url)
        self.table = self.dynamodb.Table(table_name)

    @abstractmethod 
    def get_table(self):
        pass

    @abstractmethod
    def add_item(self, params):
        pass

    @abstractmethod
    def get_item(self, index):
        pass

    @abstractmethod    
    def update_item(self, index, param, value):
        pass

    @abstractmethod
    def delete_item(self, index):
        pass
